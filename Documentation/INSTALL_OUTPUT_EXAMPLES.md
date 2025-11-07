# Installation Script Progress Output Examples

This document shows what you'll see when running the improved installation scripts.

## quick-install.sh Output

```
🦀 OmniWordlist Pro - Quick Local Setup

▶ Checking Rust toolchain...
✓ Rust is ready (rustc 1.70.0 (9f20b87d5 2023-05-10))
  └─ Cargo: cargo 1.70.0

▶ Building OmniWordlist Pro (release mode)...
📦 First build takes 5-15 minutes (compiling dependencies)
💡 Watching compilation progress:

  ⚙️  Compiling ahash
  ⚙️  Compiling bytemuck
  ⚙️  Compiling memchr
  ⚙️  Compiling version_check
  ⚙️  Compiling proc-macro2
  ⚙️  Compiling unicode-ident
  ⚙️  Compiling quote
  ⚙️  Compiling syn
  ⚙️  Compiling serde
  ⚙️  Compiling serde_json
  ⚙️  Compiling tokio
  ⚙️  Compiling regex
  ⚙️  Compiling clap
  ⚙️  Compiling omniwordlist-pro

✓ Build completed!
✓ Binary ready at: ./target/release/omni

═══════════════════════════════════════════════════════
Setup Complete! 🎉
═══════════════════════════════════════════════════════

You can now use:

  owpro info                    # Show version
  owpro list-presets            # List presets
  owpro preview --preset pentest_default    # Preview
  owpro run --min 3 --max 5 --charset abc   # Generate

Examples:

  owpro run --preset pentest_default -o pentest.txt
  owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o out.gz
  owpro fields --categories
  owpro tui                     # Launch interactive UI

Documentation: https://github.com/AaryanBansal-dev/OmniWordlistPro
```

## install.sh Output

```
╔═══════════════════════════════════════════════════════════╗
║  🦀 OmniWordlist Pro - Installation Script         ║
╚═══════════════════════════════════════════════════════════╝

▶ Checking prerequisites...
✓ Rust is installed (1.70.0)

▶ Cloning/updating repository...
✓ Repository ready at: /home/user/.local/share/omniwordlist-pro

▶ Building binary (release mode)...
📦 First build takes 5-15 minutes (compiling dependencies)
💡 You'll see crates being compiled below:

  ⚙️  ahash
  ⚙️  bytemuck
  ⚙️  memchr
  ⚙️  version_check
  ⚙️  proc-macro2
  ⚙️  unicode-ident
  ⚙️  quote
  ⚙️  syn
  ⚙️  serde
  ⚙️  serde_json
  ⚙️  tokio
  ⚙️  regex
  ⚙️  clap
  ⚙️  omniwordlist-pro

✓ Binary built successfully!

▶ Installing globally...
✓ Installed to /usr/local/bin/owpro (no sudo needed)

▶ Verifying installation...
✓ Installation verified!

═══════════════════════════════════════════════════════
Installation Complete! 🎉
═══════════════════════════════════════════════════════

Quick Start:

  owpro info                    # Show version & features
  owpro list-presets             # List available presets
  owpro preview --preset pentest_default --sample-size 50
  owpro run --min 3 --max 5 --charset abc -o out.txt

Examples:

  # Generate pentest wordlist
  owpro run --preset pentest_default -o pentest.txt

  # Preview with meme pack
  owpro preview --preset meme_humor_pack --sample-size 100

  # Compressed output
  owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o wordlist.gz

  # List all fields
  owpro fields --categories

Documentation: 📚 https://github.com/AaryanBansal-dev/OmniWordlistPro#readme

Updates:
  To update: curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh | bash
```

## install-verbose.sh Output (Detailed Progress)

```
🦀 OmniWordlist Pro - Verbose Installation Script

▶ Checking Rust installation...
✓ Rust is installed: rustc 1.70.0 (9f20b87d5 2023-05-10)
  └─ Cargo: cargo 1.70.0

▶ Setting up repository...
ℹ Cloning repository...
✓ Repository ready at: /home/user/.local/share/omniwordlist-pro

▶ Building OmniWordlist Pro (Release Mode)

This may take 5-15 minutes on first build
(Dependencies are compiled once, subsequent builds are faster)

Compilation Progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🔗 Resolving dependencies...
  ↓ Downloading: ahash 0.8
  ⚙️  Compiling: ahash
  ⚙️  Compiling: bytemuck
  ⚙️  Compiling: memchr
  ⚙️  Compiling: version_check
  ⚙️  Compiling: proc-macro2
     (5 crates compiled in 45s)

  ⚙️  Compiling: unicode-ident
  ⚙️  Compiling: quote
  ⚙️  Compiling: syn
  ⚙️  Compiling: serde
  ⚙️  Compiling: serde_json
     (10 crates compiled in 95s)

  ⚙️  Compiling: tokio
  ⚙️  Compiling: regex
  ⚙️  Compiling: clap
  ⚙️  Compiling: ratatui
  ⚙️  Compiling: flate2
     (15 crates compiled in 145s)

  ⚙️  Compiling: zstd
  ⚙️  Compiling: bzip2
  ⚙️  Compiling: lz4
  ⚙️  Compiling: rusqlite
  ⚙️  Compiling: rocksdb
     (20 crates compiled in 195s)

  ⚙️  Compiling: omniwordlist-pro
  🔗 Linking binary...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Build completed in 420 seconds!
  └─ Compiled 52 crates

ℹ Binary source: target/release/omni
ℹ Target location: /usr/local/bin/owpro

✓ Binary created: target/release/omni (8.2M)
✓ Installed to /usr/local/bin/owpro (no sudo required)

▶ Verifying installation...
✓ owpro command is available
  └─ Version: omniwordlist-pro 1.1.0

╔═══════════════════════════════════════════════════════════════╗
║  ✅ Installation Complete!                            ║
╚═══════════════════════════════════════════════════════════════╝

Quick Start Commands:

  owpro info                    # Show version & features
  owpro list-presets             # List available presets
  owpro preview --preset pentest_default --sample-size 50

Usage Examples:

  # Generate basic wordlist
  owpro run --min 3 --max 5 --charset abc -o output.txt

  # Pentesting wordlist
  owpro run --preset pentest_default -o pentest.txt

  # Compressed output (gzip)
  owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o out.gz

  # JSON format
  owpro run --charset 'abc' --min 3 --max 4 --format jsonl -o out.jsonl

Browse Fields & Presets:

  owpro fields --categories      # List all field categories
  owpro show-preset pentest_default  # Show preset details
  owpro tui                      # Interactive TUI (experimental)

Documentation:
  📚 https://github.com/AaryanBansal-dev/OmniWordlistPro

Get Help:
  owpro --help                   # Show all commands
  owpro run --help               # Help for 'run' command
```

## What's Different Now?

### Before (Old Script):
```
▶ Building OmniWordlist Pro (this may take 2-5 minutes)...
[... nothing for 10 minutes ...]
✓ Binary built successfully!
```
❌ Users thought the script was frozen or broken

### After (New Scripts):
```
▶ Building OmniWordlist Pro (release mode)...
📦 First build takes 5-15 minutes (compiling dependencies)
💡 Watching compilation progress:

  ⚙️  Compiling ahash
  ⚙️  Compiling bytemuck
  ⚙️  Compiling memchr
  [... shows each crate ...]
✓ Build completed!
```
✅ Users can see exactly what's being compiled
✅ Progress is visible and clear
✅ No confusion about whether it's working

## Key Improvements

| Feature | Old Script | New Scripts |
|---------|-----------|-------------|
| Shows compilation progress | ❌ No | ✅ Yes (all) |
| Shows each crate | ❌ No | ✅ Yes (all) |
| Shows timing | ❌ No | ✅ Yes (verbose) |
| Shows download progress | ❌ No | ✅ Yes (verbose) |
| Shows linking status | ❌ No | ✅ Yes (verbose) |
| Colorized output | ❌ No | ✅ Yes (all) |
| Verbose error messages | ❌ No | ✅ Yes (all) |
| Binary size displayed | ❌ No | ✅ Yes (verbose) |
| Estimated time | ❌ No | ✅ Yes (verbose) |

## Running the Scripts

### Method 1: Quick Setup (Local)
```bash
cd OmniWordlistPro
./quick-install.sh
```

### Method 2: System Installation
```bash
cd OmniWordlistPro
./install.sh
```

### Method 3: Verbose Progress (Troubleshooting)
```bash
cd OmniWordlistPro
./install-verbose.sh
```

## Why No More "Frozen" Appearance?

The improved scripts use:

1. **Verbose Cargo Output** — `cargo build --release -v` shows each compilation
2. **Real-Time Streaming** — Lines are displayed as they happen, not buffered
3. **Colored Status Indicators** — ⚙️ (compiling), 🔗 (linking), ✓ (done)
4. **Progress Tracking** — Crate counts every 5 crates compiled
5. **Time Tracking** — Shows elapsed time and estimates

This gives users:
- ✅ Confidence that something is happening
- ✅ Progress visibility
- ✅ Expected completion time
- ✅ No "is it frozen?" anxiety

## Next Steps

1. **Use one of the three scripts** (quick, normal, or verbose)
2. **Watch the progress** — you'll see what's compiling
3. **First build takes 5-15 minutes** — this is normal!
4. **Subsequent builds are faster** — cached dependencies
5. **Run `owpro info`** to verify it works

See **[INSTALL_SCRIPTS.md](INSTALL_SCRIPTS.md)** for more details.
