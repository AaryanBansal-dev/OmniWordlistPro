/// OmniWordlist Pro - Enterprise-grade wordlist generation library
/// 
/// This crate provides a complete wordlist generation framework combining
/// Crunch-like pattern generation with CUPP-style personalization and
/// 1500+ toggleable fields with advanced transforms.

pub mod error;
pub mod config;
pub mod fields;
pub mod generator;
pub mod transforms;
pub mod filters;
pub mod storage;
pub mod presets;
pub mod ui;
pub mod charset;

pub use error::{Error, Result};
pub use config::Config;
pub use generator::Generator;
pub use presets::PresetManager;

#[derive(Debug, Clone)]
pub struct AppState {
    pub config: Config,
    pub preset_manager: std::sync::Arc<parking_lot::Mutex<PresetManager>>,
}

impl AppState {
    pub fn new(config: Config) -> Self {
        Self {
            config,
            preset_manager: std::sync::Arc::new(parking_lot::Mutex::new(PresetManager::new())),
        }
    }
}
