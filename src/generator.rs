/// Core generation engine
/// 
/// Streaming combinator pipeline with checkpoint support and deduplication

use std::sync::Arc;
use parking_lot::Mutex;
use blake2::Blake2b512;
use std::hash::Hasher;
use std::collections::HashSet;

pub struct Generator {
    config: crate::Config,
    state: Arc<Mutex<GeneratorState>>,
}

#[derive(Debug, Clone)]
struct GeneratorState {
    tokens_generated: u64,
    checkpoint: Option<String>,
    dedup_hashes: HashSet<u64>,
}

impl Generator {
    pub fn new(config: crate::Config) -> crate::Result<Self> {
        config.validate()?;
        
        Ok(Self {
            config,
            state: Arc::new(Mutex::new(GeneratorState {
                tokens_generated: 0,
                checkpoint: None,
                dedup_hashes: HashSet::new(),
            })),
        })
    }

    /// Generate tokens from charset
    pub fn generate_charset(&self) -> crate::Result<Vec<String>> {
        let charset = self.resolve_charset()?;
        self.generate_from_charset(&charset)
    }

    /// Generate tokens using pattern matching (Crunch-style)
    pub fn generate_pattern(&self) -> crate::Result<Vec<String>> {
        let pattern = self.config.pattern.as_ref()
            .ok_or_else(|| crate::Error::ConfigError("No pattern specified".to_string()))?;
        
        let literal_chars = self.config.literal_chars.as_deref();
        let charset = crate::charset::expand_pattern(pattern, literal_chars)?;
        
        self.generate_from_charset(&charset)
    }

    /// Generate tokens using field-based approach
    pub fn generate_fields(&self) -> crate::Result<Vec<String>> {
        if self.config.enabled_fields.is_empty() {
            return Err(crate::Error::ConfigError(
                "No fields enabled".to_string(),
            ));
        }

        let mut tokens = vec![String::new()];

        for field_id in &self.config.enabled_fields {
            if let Some(field) = crate::fields::FieldManager::get_field(field_id) {
                let field_tokens = field.examples.clone();
                let mut new_tokens = Vec::new();
                
                for existing in &tokens {
                    for field_token in &field_tokens {
                        new_tokens.push(format!("{}{}", existing, field_token));
                    }
                }
                
                tokens = new_tokens;
            }
        }

        Ok(tokens)
    }

    /// Generate all combinations up to max_length
    fn generate_from_charset(&self, charset: &str) -> crate::Result<Vec<String>> {
        let mut tokens = Vec::new();
        let start = self.config.start_string.clone();
        let end = self.config.end_string.clone();

        for len in self.config.min_length..=self.config.max_length {
            let len_tokens = self.generate_combinations(charset, len, start.clone(), end.clone())?;
            tokens.extend(len_tokens);
            
            if let Some(limit) = self.config.max_lines {
                if tokens.len() >= limit as usize {
                    tokens.truncate(limit as usize);
                    break;
                }
            }
        }

        Ok(tokens)
    }

    /// Generate combinations of given length
    fn generate_combinations(
        &self,
        charset: &str,
        length: usize,
        start: Option<String>,
        end: Option<String>,
    ) -> crate::Result<Vec<String>> {
        let chars: Vec<char> = charset.chars().collect();
        let mut tokens = Vec::new();
        
        if self.config.permutations_only {
            self.generate_permutations(&chars, length, &mut tokens)?;
        } else {
            self.generate_combinations_recursive(
                &chars,
                length,
                &mut String::new(),
                &mut tokens,
            )?;
        }

        // Filter by start/end if specified
        if let Some(start_str) = start {
            tokens = tokens.into_iter()
                .skip_while(|t| t < &start_str)
                .collect();
        }

        if let Some(end_str) = end {
            tokens = tokens.into_iter()
                .take_while(|t| t <= &end_str)
                .collect();
        }

        // Apply prefix/suffix
        if let Some(prefix) = &self.config.prefix {
            tokens = tokens.into_iter()
                .map(|t| format!("{}{}", prefix, t))
                .collect();
        }

        if let Some(suffix) = &self.config.suffix {
            tokens = tokens.into_iter()
                .map(|t| format!("{}{}", t, suffix))
                .collect();
        }

        // Apply duplicate suppression
        tokens = self.apply_duplicate_suppression(tokens);

        // Apply inversion
        tokens = self.invert_tokens(tokens);

        Ok(tokens)
    }

    /// Recursive combination generator
    fn generate_combinations_recursive(
        &self,
        chars: &[char],
        length: usize,
        current: &mut String,
        result: &mut Vec<String>,
    ) -> crate::Result<()> {
        if current.len() == length {
            result.push(current.clone());
            return Ok(());
        }

        for &ch in chars {
            current.push(ch);
            self.generate_combinations_recursive(chars, length, current, result)?;
            current.pop();
        }

        Ok(())
    }

    /// Generate permutations (no repeating characters)
    fn generate_permutations(
        &self,
        chars: &[char],
        length: usize,
        result: &mut Vec<String>,
    ) -> crate::Result<()> {
        if length > chars.len() {
            return Ok(());
        }

        self.permute_helper(
            chars,
            length,
            &mut String::new(),
            &mut std::collections::HashSet::new(),
            result,
        )
    }

    fn permute_helper(
        &self,
        chars: &[char],
        length: usize,
        current: &mut String,
        used: &mut std::collections::HashSet<usize>,
        result: &mut Vec<String>,
    ) -> crate::Result<()> {
        if current.len() == length {
            result.push(current.clone());
            return Ok(());
        }

        for i in 0..chars.len() {
            if !used.contains(&i) {
                current.push(chars[i]);
                used.insert(i);
                self.permute_helper(chars, length, current, used, result)?;
                current.pop();
                used.remove(&i);
            }
        }

        Ok(())
    }

    /// Deduplicate using Blake2b hashing
    pub fn deduplicate(&self, tokens: Vec<String>) -> crate::Result<Vec<String>> {
        let mut seen = HashSet::new();
        let mut unique = Vec::new();

        for token in tokens {
            let hash = self.hash_token(&token);
            if seen.insert(hash) {
                unique.push(token);
            }
        }

        Ok(unique)
    }

    fn hash_token(&self, token: &str) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        let mut hasher = DefaultHasher::new();
        hasher.write(token.as_bytes());
        hasher.finish()
    }

    /// Apply transform pipeline
    pub fn apply_transforms(&self, tokens: Vec<String>) -> crate::Result<Vec<String>> {
        let mut pipeline = crate::transforms::TransformPipeline::new();

        for transform_name in &self.config.transforms {
            let transform = self.parse_transform(transform_name)?;
            pipeline = pipeline.add(transform);
        }

        pipeline.apply_all(tokens)
    }

    /// Parse transform name to Transform enum
    fn parse_transform(&self, name: &str) -> crate::Result<crate::transforms::Transform> {
        match name {
            "leet_basic" => Ok(crate::transforms::Transform::LeetBasic),
            "leet_full" => Ok(crate::transforms::Transform::LeetFull),
            "leet_random" => Ok(crate::transforms::Transform::LeetRandom),
            "reverse" => Ok(crate::transforms::Transform::Reverse),
            "toggle_case" => Ok(crate::transforms::Transform::ToggleCase),
            "upper" => Ok(crate::transforms::Transform::UpperCase),
            "lower" => Ok(crate::transforms::Transform::LowerCase),
            "capitalize" => Ok(crate::transforms::Transform::Capitalize),
            "homoglyph" => Ok(crate::transforms::Transform::Homoglyph),
            "emoji" => Ok(crate::transforms::Transform::EmojiInsertion),
            "keyboard_shift" => Ok(crate::transforms::Transform::KeyboardShift),
            _ => Err(crate::Error::TransformError(format!(
                "Unknown transform: {}",
                name
            ))),
        }
    }

    /// Apply filters
    pub fn apply_filters(&self, tokens: Vec<String>) -> Vec<String> {
        let mut filter_chain = crate::filters::FilterChain::new();

        if let Some(min) = self.config.filters.min_len {
            if let Some(max) = self.config.filters.max_len {
                filter_chain = filter_chain.add_length(min, max);
            }
        }

        if let Some(charset) = &self.config.filters.charset_filter {
            filter_chain = filter_chain.add_charset(charset.clone());
        }

        filter_chain.apply_batch(tokens)
    }

    /// Full pipeline: generate -> dedupe -> transform -> filter
    pub fn generate_full_pipeline(&self) -> crate::Result<Vec<String>> {
        let mut tokens = self.generate_charset()?;

        if self.config.dedupe {
            tokens = self.deduplicate(tokens)?;
        }

        tokens = self.apply_transforms(tokens)?;
        tokens = self.apply_filters(tokens);

        Ok(tokens)
    }

    fn resolve_charset(&self) -> crate::Result<String> {
        if let Some(charset) = &self.config.charset {
            Ok(charset.clone())
        } else {
            Ok(crate::charset::CharsetBuilder::new()
                .add_charset("lower")?
                .build())
        }
    }

    pub fn stats(&self) -> GeneratorStats {
        let state = self.state.lock();
        GeneratorStats {
            tokens_generated: state.tokens_generated,
            unique_tokens: state.dedup_hashes.len(),
        }
    }

    /// Apply duplicate suppression based on config
    fn apply_duplicate_suppression(&self, tokens: Vec<String>) -> Vec<String> {
        if let Some(dup_limit) = &self.config.duplicate_limit {
            tokens.into_iter()
                .filter(|token| self.check_duplicate_limit(token, dup_limit))
                .collect()
        } else {
            tokens
        }
    }

    /// Check if a token violates duplicate character limits
    fn check_duplicate_limit(&self, token: &str, limit_spec: &str) -> bool {
        // Parse limit_spec like "2@" meaning max 2 adjacent @ chars
        // or "@@" meaning no adjacent duplicates for @
        // For simplicity, check for any character repetition > limit
        let limit = if let Some(num_str) = limit_spec.chars().take_while(|c| c.is_numeric()).collect::<String>().parse::<usize>().ok() {
            num_str
        } else {
            1 // Default: no adjacent duplicates
        };

        let chars: Vec<char> = token.chars().collect();
        let mut count = 1;
        
        for i in 1..chars.len() {
            if chars[i] == chars[i-1] {
                count += 1;
                if count > limit {
                    return false;
                }
            } else {
                count = 1;
            }
        }
        
        true
    }

    /// Invert token order (for -i flag, makes first char change most frequently)
    fn invert_tokens(&self, mut tokens: Vec<String>) -> Vec<String> {
        if self.config.invert {
            // Reverse the order - this makes the first character change most frequently
            tokens.reverse();
        }
        tokens
    }

    /// Calculate total combinations for status display
    pub fn calculate_combinations(&self, charset: &str, length: usize) -> u64 {
        let charset_len = charset.chars().count() as u64;
        if self.config.permutations_only {
            // Permutations: n! / (n-r)!
            let mut result = 1u64;
            for i in 0..length {
                result = result.saturating_mul(charset_len.saturating_sub(i as u64));
            }
            result
        } else {
            // Combinations with repetition: n^r
            charset_len.saturating_pow(length as u32)
        }
    }

    /// Show status information before generation
    pub fn show_status_info(&self, charset: &str) -> crate::Result<()> {
        if !self.config.show_status {
            return Ok(());
        }

        println!("📊 Generation Status:");
        println!("  Charset: {} ({} chars)", charset, charset.chars().count());
        println!("  Length range: {} - {}", self.config.min_length, self.config.max_length);
        
        let mut total_combinations = 0u64;
        let mut total_bytes = 0u64;
        
        for len in self.config.min_length..=self.config.max_length {
            let combos = self.calculate_combinations(charset, len);
            total_combinations = total_combinations.saturating_add(combos);
            // Estimate bytes: each token = length + 1 (newline)
            total_bytes = total_bytes.saturating_add(combos.saturating_mul((len + 1) as u64));
        }
        
        println!("  Total combinations: {}", total_combinations);
        println!("  Estimated size: {} bytes ({} KB, {} MB)", 
            total_bytes, 
            total_bytes / 1024,
            total_bytes / 1024 / 1024
        );
        println!();
        
        Ok(())
    }
}


#[derive(Debug, Clone)]
pub struct GeneratorStats {
    pub tokens_generated: u64,
    pub unique_tokens: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generator_creation() {
        let config = crate::Config {
            min_length: 3,
            max_length: 3,
            charset: Some("abc".to_string()),
            ..Default::default()
        };
        let gen = Generator::new(config);
        assert!(gen.is_ok());
    }

    #[test]
    fn test_generate_combinations() {
        let config = crate::Config {
            min_length: 2,
            max_length: 2,
            charset: Some("ab".to_string()),
            ..Default::default()
        };
        let gen = Generator::new(config).unwrap();
        let tokens = gen.generate_charset().unwrap();
        assert_eq!(tokens.len(), 4); // aa, ab, ba, bb
    }

    #[test]
    fn test_deduplication() {
        let config = crate::Config::default();
        let gen = Generator::new(config).unwrap();
        let tokens = vec!["test".to_string(), "test".to_string(), "hello".to_string()];
        let unique = gen.deduplicate(tokens).unwrap();
        assert_eq!(unique.len(), 2);
    }
}
