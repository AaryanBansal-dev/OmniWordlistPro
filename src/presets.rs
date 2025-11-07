/// Preset management system
/// 
/// Save and load wordlist generation presets

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Preset {
    pub name: String,
    pub description: String,
    pub version: String,
    pub config: crate::Config,
    pub tags: Vec<String>,
    pub created_at: String,
    pub updated_at: String,
}

pub struct PresetManager {
    presets: HashMap<String, Preset>,
    presets_dir: std::path::PathBuf,
}

impl PresetManager {
    pub fn new() -> Self {
        let mut manager = Self {
            presets: HashMap::new(),
            presets_dir: std::path::PathBuf::from("./presets"),
        };
        
        // Load built-in presets
        manager.load_builtin_presets();
        manager
    }

    pub fn with_dir(presets_dir: impl AsRef<Path>) -> Self {
        let mut manager = Self {
            presets: HashMap::new(),
            presets_dir: presets_dir.as_ref().to_path_buf(),
        };
        
        let _ = manager.load_from_disk();
        manager
    }

    fn load_builtin_presets(&mut self) {
        // Pentest preset
        self.presets.insert(
            "pentest_default".to_string(),
            Preset {
                name: "Pentest Default".to_string(),
                description: "Standard penetration testing wordlist generation".to_string(),
                version: "1.0".to_string(),
                config: crate::Config {
                    min_length: 8,
                    max_length: 16,
                    charset: Some("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%".to_string()),
                    transforms: vec![
                        "capitalize".to_string(),
                        "append_numbers_4".to_string(),
                    ],
                    enabled_fields: vec![
                        "first_name_male_0".to_string(),
                        "last_name_0".to_string(),
                    ],
                    ..Default::default()
                },
                tags: vec!["pentest".to_string(), "default".to_string()],
                created_at: chrono::Local::now().to_rfc3339(),
                updated_at: chrono::Local::now().to_rfc3339(),
            },
        );

        // Meme humor pack
        self.presets.insert(
            "meme_humor_pack".to_string(),
            Preset {
                name: "Meme & Humor Pack".to_string(),
                description: "Creative wordlist with memes and humor".to_string(),
                version: "1.0".to_string(),
                config: crate::Config {
                    min_length: 3,
                    max_length: 140,
                    transforms: vec![
                        "random_case".to_string(),
                        "emoji_insertion".to_string(),
                    ],
                    enabled_fields: vec![
                        "meme_format_0".to_string(),
                        "emoji_smile_0".to_string(),
                    ],
                    ..Default::default()
                },
                tags: vec!["humor".to_string(), "creative".to_string()],
                created_at: chrono::Local::now().to_rfc3339(),
                updated_at: chrono::Local::now().to_rfc3339(),
            },
        );

        // API/Dev preset
        self.presets.insert(
            "api_dev_wordlist".to_string(),
            Preset {
                name: "API/Developer Wordlist".to_string(),
                description: "For testing API endpoints and developer resources".to_string(),
                version: "1.0".to_string(),
                config: crate::Config {
                    min_length: 4,
                    max_length: 20,
                    charset: Some("abcdefghijklmnopqrstuvwxyz0123456789_-".to_string()),
                    transforms: vec!["lower".to_string()],
                    enabled_fields: vec![
                        "dev_handle_0".to_string(),
                        "keyboard_walk_0".to_string(),
                    ],
                    ..Default::default()
                },
                tags: vec!["api".to_string(), "dev".to_string()],
                created_at: chrono::Local::now().to_rfc3339(),
                updated_at: chrono::Local::now().to_rfc3339(),
            },
        );

        // Social media preset
        self.presets.insert(
            "social_media_usernames".to_string(),
            Preset {
                name: "Social Media Usernames".to_string(),
                description: "Generate social media handles and usernames".to_string(),
                version: "1.0".to_string(),
                config: crate::Config {
                    min_length: 3,
                    max_length: 32,
                    charset: Some("abcdefghijklmnopqrstuvwxyz0123456789_".to_string()),
                    transforms: vec!["lower".to_string()],
                    enabled_fields: vec![
                        "social_platform_0".to_string(),
                        "dev_handle_0".to_string(),
                    ],
                    ..Default::default()
                },
                tags: vec!["social".to_string(), "usernames".to_string()],
                created_at: chrono::Local::now().to_rfc3339(),
                updated_at: chrono::Local::now().to_rfc3339(),
            },
        );

        // Pattern-based preset
        self.presets.insert(
            "pattern_basic".to_string(),
            Preset {
                name: "Pattern-Based Basic".to_string(),
                description: "Simple pattern-based generation (Crunch-style)".to_string(),
                version: "1.0".to_string(),
                config: crate::Config {
                    min_length: 4,
                    max_length: 8,
                    pattern: Some("pass@@%%".to_string()),
                    ..Default::default()
                },
                tags: vec!["pattern".to_string(), "crunch".to_string()],
                created_at: chrono::Local::now().to_rfc3339(),
                updated_at: chrono::Local::now().to_rfc3339(),
            },
        );
    }

    /// Get preset by name
    pub fn get(&self, name: &str) -> Option<Preset> {
        self.presets.get(name).cloned()
    }

    /// List all preset names
    pub fn list_names(&self) -> Vec<String> {
        self.presets.keys().cloned().collect()
    }

    /// List all presets
    pub fn list_all(&self) -> Vec<Preset> {
        self.presets.values().cloned().collect()
    }

    /// Get presets by tag
    pub fn by_tag(&self, tag: &str) -> Vec<Preset> {
        self.presets
            .values()
            .filter(|p| p.tags.contains(&tag.to_string()))
            .cloned()
            .collect()
    }

    /// Save preset
    pub fn save(&mut self, preset: Preset) -> crate::Result<()> {
        self.presets.insert(preset.name.clone(), preset.clone());
        self.save_to_disk(&preset)
    }

    /// Delete preset
    pub fn delete(&mut self, name: &str) -> crate::Result<()> {
        self.presets.remove(name);
        
        let path = self.presets_dir.join(format!("{}.json", name));
        if path.exists() {
            std::fs::remove_file(path)?;
        }
        
        Ok(())
    }

    /// Save preset to disk
    fn save_to_disk(&self, preset: &Preset) -> crate::Result<()> {
        std::fs::create_dir_all(&self.presets_dir)?;
        let path = self.presets_dir.join(format!("{}.json", preset.name));
        let json = serde_json::to_string_pretty(preset)?;
        std::fs::write(path, json)?;
        Ok(())
    }

    /// Load all presets from disk
    fn load_from_disk(&mut self) -> crate::Result<()> {
        if !self.presets_dir.exists() {
            return Ok(());
        }

        for entry in std::fs::read_dir(&self.presets_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("json") {
                if let Ok(content) = std::fs::read_to_string(&path) {
                    if let Ok(preset) = serde_json::from_str::<Preset>(&content) {
                        self.presets.insert(preset.name.clone(), preset);
                    }
                }
            }
        }

        Ok(())
    }

    /// Export preset to JSON string
    pub fn export_json(&self, name: &str) -> crate::Result<String> {
        if let Some(preset) = self.presets.get(name) {
            Ok(serde_json::to_string_pretty(preset)?)
        } else {
            Err(crate::Error::PresetError(format!(
                "Preset not found: {}",
                name
            )))
        }
    }

    /// Export preset to TOML string
    pub fn export_toml(&self, name: &str) -> crate::Result<String> {
        if let Some(preset) = self.presets.get(name) {
            Ok(toml::to_string_pretty(preset)?)
        } else {
            Err(crate::Error::PresetError(format!(
                "Preset not found: {}",
                name
            )))
        }
    }

    /// Import preset from JSON string
    pub fn import_json(&mut self, json: &str) -> crate::Result<()> {
        let preset = serde_json::from_str::<Preset>(json)?;
        self.save(preset)?;
        Ok(())
    }

    /// Merge two presets
    pub fn merge(&mut self, name1: &str, name2: &str, output_name: &str) -> crate::Result<()> {
        let preset1 = self.get(name1)
            .ok_or_else(|| crate::Error::PresetError(format!("Preset not found: {}", name1)))?;
        let preset2 = self.get(name2)
            .ok_or_else(|| crate::Error::PresetError(format!("Preset not found: {}", name2)))?;

        let mut merged_config = preset1.config;
        merged_config.enabled_fields.extend(preset2.config.enabled_fields);
        merged_config.transforms.extend(preset2.config.transforms);

        let merged = Preset {
            name: output_name.to_string(),
            description: format!(
                "Merged: {} + {}",
                preset1.description, preset2.description
            ),
            version: "1.0".to_string(),
            config: merged_config,
            tags: {
                let mut tags = preset1.tags;
                tags.extend(preset2.tags);
                tags.sort();
                tags.dedup();
                tags
            },
            created_at: chrono::Local::now().to_rfc3339(),
            updated_at: chrono::Local::now().to_rfc3339(),
        };

        self.save(merged)?;
        Ok(())
    }

    /// Estimate cardinality of preset
    pub fn estimate_cardinality(&self, name: &str) -> crate::Result<u64> {
        if let Some(preset) = self.get(name) {
            let field_cardinality = crate::fields::FieldManager::estimate_cardinality(
                &preset.config.enabled_fields
            ) as u64;
            
            let charset_cardinality = if let Some(charset) = &preset.config.charset {
                charset.len() as u64
            } else {
                26 // default lowercase
            };

            let range = (preset.config.max_length - preset.config.min_length + 1) as u64;
            let combinations = charset_cardinality.pow(range as u32);

            Ok((field_cardinality + combinations).min(u64::MAX))
        } else {
            Err(crate::Error::PresetError(format!(
                "Preset not found: {}",
                name
            )))
        }
    }
}

impl Default for PresetManager {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_preset_manager() {
        let manager = PresetManager::new();
        assert!(manager.get("pentest_default").is_some());
    }

    #[test]
    fn test_list_presets() {
        let manager = PresetManager::new();
        let names = manager.list_names();
        assert!(names.len() > 0);
        assert!(names.contains(&"pentest_default".to_string()));
    }

    #[test]
    fn test_by_tag() {
        let manager = PresetManager::new();
        let pentest_presets = manager.by_tag("pentest");
        assert!(pentest_presets.len() > 0);
    }
}
