use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    /// Minimum length of generated tokens
    pub min_length: usize,
    
    /// Maximum length of generated tokens
    pub max_length: usize,
    
    /// Custom charset for generation
    pub charset: Option<String>,
    
    /// Pattern/template (Crunch-style: @=lower, %=digit, ^=symbol)
    pub pattern: Option<String>,
    
    /// Starting point for generation (resume)
    pub start_string: Option<String>,
    
    /// Ending point for generation
    pub end_string: Option<String>,
    
    /// Output file path
    pub output_file: Option<PathBuf>,
    
    /// Compression format (gzip, bzip2, lz4, zstd)
    pub compression: Option<String>,
    
    /// Maximum output file size in bytes
    pub max_bytes: Option<u64>,
    
    /// Maximum lines to output
    pub max_lines: Option<u64>,
    
    /// Suppress duplicate adjacent characters (e.g., "2@" means max 2 adjacent @)
    pub duplicate_limit: Option<String>,
    
    /// Enable permutations (no repeating characters)
    pub permutations_only: bool,
    
    /// Invert output (first character changes frequently)
    pub invert: bool,
    
    /// Prefix to add to each token
    pub prefix: Option<String>,
    
    /// Suffix to add to each token
    pub suffix: Option<String>,
    
    /// Separator character when combining sets
    pub separator: Option<char>,
    
    /// Enabled fields for field-based generation
    pub enabled_fields: Vec<String>,
    
    /// Transform pipeline names
    pub transforms: Vec<String>,
    
    /// Filter specifications
    pub filters: FilterConfig,
    
    /// Number of parallel workers
    pub workers: usize,
    
    /// Checkpoint directory for resume capability
    pub checkpoint_dir: Option<PathBuf>,
    
    /// Enable deduplication
    pub dedupe: bool,
    
    /// Bloom filter false positive rate (0.0-1.0)
    pub bloom_fp_rate: f64,
    
    /// Buffer size for streaming
    pub buffer_size: usize,
    
    /// Enable verbose logging
    pub verbose: bool,
    
    /// Enable colorized output
    pub colorized: bool,
    
    /// Random seed for reproducible generation
    pub seed: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FilterConfig {
    pub min_len: Option<usize>,
    pub max_len: Option<usize>,
    pub charset_filter: Option<String>,
    pub exclude_charset: Option<String>,
    pub regex_pattern: Option<String>,
    pub entropy_min: Option<f64>,
    pub language_filter: Option<String>,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            min_length: 1,
            max_length: 10,
            charset: None,
            pattern: None,
            start_string: None,
            end_string: None,
            output_file: None,
            compression: None,
            max_bytes: None,
            max_lines: None,
            duplicate_limit: None,
            permutations_only: false,
            invert: false,
            prefix: None,
            suffix: None,
            separator: None,
            enabled_fields: Vec::new(),
            transforms: Vec::new(),
            filters: FilterConfig::default(),
            workers: num_cpus::get(),
            checkpoint_dir: None,
            dedupe: true,
            bloom_fp_rate: 0.01,
            buffer_size: 8192,
            verbose: false,
            colorized: true,
            seed: None,
        }
    }
}

impl Default for FilterConfig {
    fn default() -> Self {
        Self {
            min_len: None,
            max_len: None,
            charset_filter: None,
            exclude_charset: None,
            regex_pattern: None,
            entropy_min: None,
            language_filter: None,
        }
    }
}

impl Config {
    pub fn validate(&self) -> crate::Result<()> {
        if self.min_length > self.max_length {
            return Err(crate::Error::ConfigError(
                "min_length must be <= max_length".to_string(),
            ));
        }

        if self.min_length == 0 {
            return Err(crate::Error::ConfigError(
                "min_length must be > 0".to_string(),
            ));
        }

        if self.max_length > 1000 {
            return Err(crate::Error::ConfigError(
                "max_length > 1000 is not recommended".to_string(),
            ));
        }

        Ok(())
    }

    pub fn from_file(path: &std::path::Path) -> crate::Result<Self> {
        let content = std::fs::read_to_string(path)?;
        
        if path.extension().and_then(|s| s.to_str()) == Some("json") {
            serde_json::from_str(&content).map_err(|e| e.into())
        } else if path.extension().and_then(|s| s.to_str()) == Some("toml") {
            toml::from_str(&content).map_err(|e| crate::Error::ConfigError(e.to_string()))
        } else {
            Err(crate::Error::ConfigError(
                "Unsupported config format. Use .json or .toml".to_string(),
            ))
        }
    }

    pub fn to_file(&self, path: &std::path::Path) -> crate::Result<()> {
        let content = serde_json::to_string_pretty(self)?;
        std::fs::write(path, content)?;
        Ok(())
    }
}
