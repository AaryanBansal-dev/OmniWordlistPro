/// Filtering and quality control
/// 
/// Implements entropy, entropy, language detection, regex validation,
/// and other quality filters.

use regex::Regex;
use std::collections::HashSet;

pub struct FilterChain {
    filters: Vec<Box<dyn Fn(&str) -> bool>>,
}

impl FilterChain {
    pub fn new() -> Self {
        Self {
            filters: Vec::new(),
        }
    }

    pub fn add_length(mut self, min: usize, max: usize) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            let len = s.len();
            len >= min && len <= max
        }));
        self
    }

    pub fn add_charset(mut self, allowed: String) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            s.chars().all(|c| allowed.contains(c))
        }));
        self
    }

    pub fn add_exclude_charset(mut self, forbidden: String) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            !s.chars().any(|c| forbidden.contains(c))
        }));
        self
    }

    pub fn add_regex(mut self, pattern: &str) -> crate::Result<Self> {
        let regex = Regex::new(pattern)?;
        self.filters.push(Box::new(move |s: &str| regex.is_match(s)));
        Ok(self)
    }

    pub fn add_entropy_min(mut self, min_entropy: f64) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            calculate_entropy(s) >= min_entropy
        }));
        self
    }

    pub fn add_entropy_max(mut self, max_entropy: f64) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            calculate_entropy(s) <= max_entropy
        }));
        self
    }

    pub fn add_no_repeats(mut self, max_repeats: usize) -> Self {
        self.filters.push(Box::new(move |s: &str| {
            let mut max_consecutive = 0;
            let mut current_consecutive = 1;
            let mut prev_char = ' ';
            
            for ch in s.chars() {
                if ch == prev_char {
                    current_consecutive += 1;
                } else {
                    max_consecutive = max_consecutive.max(current_consecutive);
                    current_consecutive = 1;
                    prev_char = ch;
                }
            }
            max_consecutive = max_consecutive.max(current_consecutive);
            max_consecutive <= max_repeats
        }));
        self
    }

    pub fn add_profanity_check(mut self) -> Self {
        let profanities = vec![
            "badword1", "badword2", "offensive1",
        ];
        let profanity_set: HashSet<_> = profanities.into_iter().collect();
        
        self.filters.push(Box::new(move |s: &str| {
            !profanity_set.contains(s.to_lowercase().as_str())
        }));
        self
    }

    pub fn add_no_common_patterns(mut self) -> Self {
        self.filters.push(Box::new(|s: &str| {
            let common_patterns = vec![
                "123", "abc", "qwerty", "aaa", "111", "password",
            ];
            !common_patterns.iter().any(|p| s.to_lowercase().contains(p))
        }));
        self
    }

    pub fn apply(&self, token: &str) -> bool {
        self.filters.iter().all(|f| f(token))
    }

    pub fn apply_batch(&self, tokens: Vec<String>) -> Vec<String> {
        tokens.into_iter()
            .filter(|t| self.apply(t))
            .collect()
    }
}

/// Calculate Shannon entropy of a string
pub fn calculate_entropy(s: &str) -> f64 {
    let len = s.len() as f64;
    if len == 0.0 {
        return 0.0;
    }

    let mut freq = std::collections::HashMap::new();
    for ch in s.chars() {
        *freq.entry(ch).or_insert(0.0) += 1.0;
    }

    let mut entropy = 0.0;
    for count in freq.values() {
        let p = count / len;
        entropy -= p * p.log2();
    }

    entropy
}

/// Check if string is likely pronounceable
pub fn is_pronounceable(s: &str) -> bool {
    let vowels = "aeiouAEIOU";
    let consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ";
    
    let mut has_vowel = false;
    let mut has_consonant = false;
    
    for ch in s.chars() {
        if vowels.contains(ch) {
            has_vowel = true;
        }
        if consonants.contains(ch) {
            has_consonant = true;
        }
    }
    
    has_vowel && has_consonant
}

/// Estimate language of a string
pub fn detect_language(s: &str) -> &'static str {
    let lower = s.to_lowercase();
    
    // Simple heuristic-based detection
    if lower.chars().filter(|c| c.is_ascii()).count() as f64 / s.len() as f64 > 0.8 {
        "english"
    } else if lower.contains('ь') || lower.contains('ы') {
        "russian"
    } else if lower.contains('ü') || lower.contains('ä') || lower.contains('ö') {
        "german"
    } else if lower.contains('é') || lower.contains('ê') || lower.contains('ç') {
        "french"
    } else if lower.contains('ñ') || lower.contains('á') {
        "spanish"
    } else {
        "unknown"
    }
}

/// Check visual similarity to common patterns
pub fn visual_similarity_score(s: &str) -> f64 {
    let similar_pairs = vec![
        ("0", "o"), ("1", "l"), ("1", "i"), 
        ("5", "s"), ("7", "t"), ("8", "b"),
    ];
    
    let mut similarity: f64 = 0.0;
    for (pair1, pair2) in similar_pairs {
        if s.contains(pair1) && s.contains(pair2) {
            similarity += 0.1;
        }
    }
    
    similarity.min(1.0)
}

/// Calculate edit distance (Levenshtein)
pub fn levenshtein_distance(s1: &str, s2: &str) -> usize {
    levenshtein::levenshtein(s1, s2)
}

/// Check if string matches common patterns
pub fn matches_common_pattern(s: &str) -> bool {
    let patterns = vec![
        "password", "admin", "letmein", "welcome", "123456",
        "qwerty", "dragon", "master", "sunshine", "princess",
    ];
    
    let lower = s.to_lowercase();
    patterns.iter().any(|p| lower.contains(p))
}

/// Rate overall quality of a token (0.0 - 1.0)
pub fn quality_score(token: &str) -> f64 {
    let mut score = 0.5;
    
    // Length bonus
    if token.len() >= 8 {
        score += 0.2;
    }
    
    // Entropy bonus
    let entropy = calculate_entropy(token);
    score += (entropy / 5.0).min(0.3);
    
    // Pronounceability
    if is_pronounceable(token) {
        score += 0.1;
    }
    
    // Penalty for common patterns
    if matches_common_pattern(token) {
        score -= 0.3;
    }
    
    score.max(0.0).min(1.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entropy() {
        let entropy_random = calculate_entropy("xkcd");
        let entropy_repeat = calculate_entropy("aaaa");
        assert!(entropy_random > entropy_repeat);
    }

    #[test]
    fn test_pronounceable() {
        assert!(is_pronounceable("hello"));
        assert!(!is_pronounceable("xy"));
    }

    #[test]
    fn test_quality_score() {
        let score = quality_score("password");
        assert!(score < 0.5); // Should be low due to common pattern
        
        let score2 = quality_score("xB7k!mQ");
        assert!(score2 > 0.5); // Should be high
    }

    #[test]
    fn test_filter_chain() {
        let filter = FilterChain::new()
            .add_length(5, 10);
        
        assert!(filter.apply("hello"));
        assert!(!filter.apply("hi"));
        assert!(!filter.apply("verylongword"));
    }
}
