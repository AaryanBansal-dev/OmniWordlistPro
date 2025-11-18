use clap::{Parser, Subcommand};
use omniwordlist::{Config, Generator, AppState};
use std::path::PathBuf;
use colored::Colorize;

#[derive(Parser)]
#[command(name = "OmniWordlist Pro")]
#[command(about = "Enterprise-grade wordlist generation in Rust")]
#[command(version = "1.1.0")]
#[command(author = "Aaryan Bansal")]
struct Cli {
    #[command(subcommand)]
    command: Commands,

    /// Verbose output
    #[arg(short, long, global = true)]
    verbose: bool,

    /// Enable colorized output
    #[arg(long, global = true, default_value = "true")]
    colorize: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Run wordlist generation
    Run {
        /// Minimum length
        #[arg(short, long)]
        min: Option<usize>,

        /// Maximum length
        #[arg(short, long)]
        max: Option<usize>,

        /// Charset
        #[arg(short, long)]
        charset: Option<String>,

        /// Pattern (Crunch-style)
        #[arg(short, long)]
        pattern: Option<String>,

        /// Output file
        #[arg(short, long)]
        output: Option<PathBuf>,

        /// Compression format (gzip, bzip2, lz4, zstd)
        #[arg(long)]
        compress: Option<String>,

        /// Prefix
        #[arg(long)]
        prefix: Option<String>,

        /// Suffix
        #[arg(long)]
        suffix: Option<String>,

        /// Enable permutations only
        #[arg(long)]
        permutations: bool,

        /// Start string (resume from this point)
        #[arg(short, long)]
        start: Option<String>,

        /// End string (stop at this point)
        #[arg(short, long)]
        end: Option<String>,

        /// Literal characters (don't expand in pattern)
        #[arg(short, long)]
        literal: Option<String>,

        /// Invert output (first char changes most frequently)
        #[arg(short, long)]
        invert: bool,

        /// Duplicate suppression (e.g., "2@" = max 2 adjacent @)
        #[arg(short, long)]
        duplicate_limit: Option<String>,

        /// Show status (count and bytes) before generation
        #[arg(long)]
        status: bool,

        /// Split output by size in bytes
        #[arg(long)]
        split_bytes: Option<u64>,

        /// Split output by number of lines
        #[arg(long)]
        split_lines: Option<u64>,

        /// Config file
        #[arg(long)]
        config: Option<PathBuf>,

        /// Preset name
        #[arg(long)]
        preset: Option<String>,
    },

    /// Preview tokens (sample)
    Preview {
        /// Number of samples
        #[arg(short, long, default_value = "100")]
        sample_size: usize,

        /// Preset name
        #[arg(long)]
        preset: Option<String>,

        /// Config file
        #[arg(long)]
        config: Option<PathBuf>,
    },

    /// List available presets
    ListPresets {
        /// Filter by tag
        #[arg(long)]
        tag: Option<String>,
    },

    /// Show preset details
    ShowPreset {
        /// Preset name
        name: String,
    },

    /// Validate configuration
    Validate {
        /// Config file
        config: PathBuf,
    },

    /// Export preset
    ExportPreset {
        /// Preset name
        preset: String,

        /// Output format (json, toml)
        #[arg(short, long, default_value = "json")]
        format: String,

        /// Output file
        #[arg(short, long)]
        output: Option<PathBuf>,
    },

    /// Generate using fields
    GenerateFields {
        /// Enabled fields (comma-separated)
        #[arg(short, long)]
        fields: Vec<String>,

        /// Output file
        #[arg(short, long)]
        output: Option<PathBuf>,

        /// Compression format
        #[arg(long)]
        compress: Option<String>,
    },

    /// Show field information
    Fields {
        /// Filter by category
        #[arg(short, long)]
        category: Option<String>,

        /// List categories only
        #[arg(long)]
        categories: bool,

        /// Search by name
        #[arg(short, long)]
        search: Option<String>,
    },

    /// Interactive TUI
    Tui,

    /// Show version and features
    Info,
}

fn main() -> omniwordlist::Result<()> {
    let cli = Cli::parse();

    if cli.verbose {
        println!("Verbose mode enabled");
    }

    // Print banner
    if !matches!(cli.command, Commands::Info) {
        omniwordlist::ui::print_banner();
    }

    match cli.command {
        Commands::Run {
            min,
            max,
            charset,
            pattern,
            output,
            compress,
            prefix,
            suffix,
            permutations,
            start,
            end,
            literal,
            invert,
            duplicate_limit,
            status,
            split_bytes,
            split_lines,
            config: config_path,
            preset,
        } => {
            let mut config = if let Some(path) = config_path {
                Config::from_file(&path)?
            } else if let Some(preset_name) = preset {
                let manager = omniwordlist::presets::PresetManager::new();
                manager.get(&preset_name)
                    .ok_or_else(|| omniwordlist::Error::PresetError(
                        format!("Preset not found: {}", preset_name)
                    ))?
                    .config
            } else {
                Config::default()
            };

            if let Some(m) = min {
                config.min_length = m;
            }
            if let Some(m) = max {
                config.max_length = m;
            }
            if let Some(c) = charset {
                config.charset = Some(c);
            }
            if let Some(p) = pattern {
                config.pattern = Some(p);
            }
            if let Some(o) = output {
                config.output_file = Some(o);
            }
            if let Some(c) = compress {
                config.compression = Some(c);
            }
            if let Some(p) = prefix {
                config.prefix = Some(p);
            }
            if let Some(s) = suffix {
                config.suffix = Some(s);
            }
            if permutations {
                config.permutations_only = true;
            }
            if let Some(s) = start {
                config.start_string = Some(s);
            }
            if let Some(e) = end {
                config.end_string = Some(e);
            }
            if let Some(l) = literal {
                config.literal_chars = Some(l);
            }
            if invert {
                config.invert = true;
            }
            if let Some(d) = duplicate_limit {
                config.duplicate_limit = Some(d);
            }
            if status {
                config.show_status = true;
            }
            if let Some(sb) = split_bytes {
                config.split_by_bytes = Some(sb);
            }
            if let Some(sl) = split_lines {
                config.split_by_lines = Some(sl);
            }

            config.verbose = cli.verbose;
            config.colorized = cli.colorize;

            run_generation(config)?;
        }

        Commands::Preview { sample_size, preset, config: config_path } => {
            let mut config = if let Some(path) = config_path {
                Config::from_file(&path)?
            } else if let Some(preset_name) = preset {
                let manager = omniwordlist::presets::PresetManager::new();
                manager.get(&preset_name)
                    .ok_or_else(|| omniwordlist::Error::PresetError(
                        format!("Preset not found: {}", preset_name)
                    ))?
                    .config
            } else {
                Config::default()
            };

            config.max_lines = Some(sample_size as u64);
            config.verbose = cli.verbose;
            config.colorized = cli.colorize;

            preview_tokens(config)?;
        }

        Commands::ListPresets { tag } => {
            list_presets(tag)?;
        }

        Commands::ShowPreset { name } => {
            show_preset(&name)?;
        }

        Commands::Validate { config: config_path } => {
            let config = Config::from_file(&config_path)?;
            config.validate()?;
            println!("✓ Configuration is valid");
        }

        Commands::ExportPreset { preset, format, output } => {
            export_preset(&preset, &format, output)?;
        }

        Commands::GenerateFields { fields, output, compress } => {
            let mut config = Config::default();
            config.enabled_fields = fields;
            if let Some(o) = output {
                config.output_file = Some(o);
            }
            if let Some(c) = compress {
                config.compression = Some(c);
            }
            config.verbose = cli.verbose;
            config.colorized = cli.colorize;

            run_generation(config)?;
        }

        Commands::Fields { category, categories, search } => {
            show_fields(category, categories, search)?;
        }

        Commands::Tui => {
            run_tui()?;
        }

        Commands::Info => {
            show_info();
        }
    }

    Ok(())
}

fn run_generation(config: Config) -> omniwordlist::Result<()> {
    config.validate()?;

    let generator = Generator::new(config.clone())?;

    // Show status if requested
    if config.show_status {
        let charset = if let Some(c) = &config.charset {
            c.clone()
        } else {
            omniwordlist::charset::CharsetBuilder::new()
                .add_charset("lower")?
                .build()
        };
        generator.show_status_info(&charset)?;
    }

    if config.verbose {
        println!("📝 Configuration:");
        println!("  Min Length: {}", config.min_length);
        println!("  Max Length: {}", config.max_length);
        if let Some(charset) = &config.charset {
            println!("  Charset: {} (size: {})", charset, charset.chars().count());
        }
        if let Some(pattern) = &config.pattern {
            println!("  Pattern: {}", pattern);
        }
        if config.invert {
            println!("  Invert: enabled");
        }
        if let Some(dup) = &config.duplicate_limit {
            println!("  Duplicate suppression: {}", dup);
        }
        println!("  Transforms: {:?}", config.transforms);
        println!("  Dedupe: {}", config.dedupe);
        println!();
    }

    if config.verbose {
        println!("🔧 Generating...");
    }

    let tokens = if !config.pattern.is_none() {
        generator.generate_pattern()?
    } else if !config.enabled_fields.is_empty() {
        generator.generate_fields()?
    } else {
        generator.generate_charset()?
    };

    if config.verbose {
        println!("📊 Generated: {} tokens", tokens.len());
        println!("📦 Applying transforms...");
    }

    let transformed = if !config.transforms.is_empty() {
        generator.apply_transforms(tokens)?
    } else {
        tokens
    };

    if config.verbose {
        println!("🔍 Applying filters...");
    }

    let filtered = generator.apply_filters(transformed);

    if config.verbose {
        println!("✓ Final count: {} tokens", filtered.len());
    }

    // Write output
    if let Some(output_path) = config.output_file {
        if config.verbose {
            println!("💾 Writing to: {}", output_path.display());
        }

        let writer = omniwordlist::storage::StorageWriter::new(
            &output_path,
            config.compression,
        );

        writer.write_tokens(&filtered)?;

        if config.verbose {
            println!("✓ Wordlist saved successfully!");
        }
    } else {
        // Output to stdout
        for token in filtered.iter().take(100) {
            println!("{}", token);
        }
        if filtered.len() > 100 {
            println!("\n... and {} more tokens (use -o to save to file)", filtered.len() - 100);
        }
    }

    Ok(())
}

fn preview_tokens(config: Config) -> omniwordlist::Result<()> {
    config.validate()?;

    let generator = Generator::new(config.clone())?;
    let tokens = if !config.pattern.is_none() {
        generator.generate_pattern()?
    } else if !config.enabled_fields.is_empty() {
        generator.generate_fields()?
    } else {
        generator.generate_charset()?
    };

    let to_show = tokens.iter().take(config.max_lines.unwrap_or(100) as usize);

    println!("📋 Token Preview:");
    println!();

    for (i, token) in to_show.enumerate() {
        let entropy = omniwordlist::filters::calculate_entropy(token);
        let quality = omniwordlist::filters::quality_score(token);
        
        println!("{:3}. {} [E: {:.2}, Q: {:.2}]", i + 1, token, entropy, quality);
    }

    Ok(())
}

fn list_presets(tag: Option<String>) -> omniwordlist::Result<()> {
    let manager = omniwordlist::presets::PresetManager::new();

    let presets = if let Some(tag_filter) = tag {
        manager.by_tag(&tag_filter)
    } else {
        manager.list_all()
    };

    println!("📚 Available Presets:");
    println!();

    for preset in presets {
        println!("  {} v{}", preset.name.cyan(), preset.version);
        println!("    {}", preset.description);
        println!("    Tags: {}", preset.tags.join(", "));
        println!();
    }

    Ok(())
}

fn show_preset(name: &str) -> omniwordlist::Result<()> {
    let manager = omniwordlist::presets::PresetManager::new();

    if let Some(preset) = manager.get(name) {
        println!("📋 Preset: {}", preset.name.cyan());
        println!("Description: {}", preset.description);
        println!("Version: {}", preset.version);
        println!("Tags: {}", preset.tags.join(", "));
        println!();
        println!("Configuration:");
        println!("{}", serde_json::to_string_pretty(&preset.config)?);
    } else {
        println!("❌ Preset not found: {}", name);
    }

    Ok(())
}

fn export_preset(preset_name: &str, format: &str, output: Option<PathBuf>) -> omniwordlist::Result<()> {
    let manager = omniwordlist::presets::PresetManager::new();

    let content = if format == "toml" {
        manager.export_toml(preset_name)?
    } else {
        manager.export_json(preset_name)?
    };

    if let Some(output_path) = output {
        std::fs::write(&output_path, &content)?;
        println!("✓ Exported to: {}", output_path.display());
    } else {
        println!("{}", content);
    }

    Ok(())
}

fn show_fields(
    category: Option<String>,
    categories: bool,
    search: Option<String>,
) -> omniwordlist::Result<()> {
    use omniwordlist::fields::FieldManager;

    if categories {
        println!("📁 Field Categories:");
        for cat in FieldManager::categories() {
            println!("  - {}", cat);
        }
        return Ok(());
    }

    if let Some(cat) = category {
        let fields = FieldManager::fields_by_category(&cat);
        println!("📊 Fields in category '{}':", cat.cyan());
        println!();

        for field in fields.iter().take(50) {
            println!("  {} [{}]", field.id.yellow(), field.group);
            if !field.examples.is_empty() {
                println!("    Examples: {}", field.examples.join(", "));
            }
        }

        if fields.len() > 50 {
            println!("  ... and {} more", fields.len() - 50);
        }
    } else if let Some(search_term) = search {
        let all_fields = FieldManager::all_fields();
        let matching: Vec<_> = all_fields.iter()
            .filter(|f| f.id.contains(&search_term) || f.description.contains(&search_term))
            .collect();

        println!("🔍 Fields matching '{}':", search_term.cyan());
        println!();

        for field in matching.iter().take(50) {
            println!("  {} [{}]", field.id.yellow(), field.group);
        }

        if matching.len() > 50 {
            println!("  ... and {} more", matching.len() - 50);
        }
    } else {
        println!("📊 Total fields available: {}", FieldManager::all_fields().len());
        println!("Use --category or --search to explore fields");
    }

    Ok(())
}

fn run_tui() -> omniwordlist::Result<()> {
    let app = omniwordlist::ui::TuiApp::new();
    println!("🎨 Launching interactive TUI...");
    println!("Note: Full TUI requires terminal interaction (coming soon)");
    println!();

    // Display dashboard info
    let state = app.state.lock();
    println!("Current Status:");
    for log in &state.logs {
        println!("  {}", log);
    }

    Ok(())
}

fn show_info() {
    omniwordlist::ui::print_banner();
    
    println!();
    println!("📦 Version: 1.1.0");
    println!("🦀 Built with Rust + Ratatui");
    println!();
    println!("✨ Features:");
    println!("  ✓ 1500+ toggleable fields");
    println!("  ✓ Crunch-compatible pattern generation");
    println!("  ✓ CUPP-style personalization");
    println!("  ✓ 100+ transform types");
    println!("  ✓ Streaming generation");
    println!("  ✓ Multi-format compression");
    println!("  ✓ Beautiful colored TUI");
    println!("  ✓ S3/MinIO support");
    println!("  ✓ Checkpointing & resume");
    println!("  ✓ Advanced filtering");
    println!();
    println!("🚀 Quick Start:");
    println!("  omni run --help");
    println!("  omni list-presets");
    println!("  omni preview --preset pentest_default");
    println!();
}
