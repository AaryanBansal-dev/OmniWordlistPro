# 🚀 OmniWordlist Pro - Complete Installation & Setup Guide

**Version:** 1.1.0  
**Last Updated:** 2025-11-07  
**Repository:** https://github.com/AaryanBansal-dev/OmniWordlistPro

---

## ⚡ Quick Start: One-Command Installation

### 🎯 Choose Your Method

Pick **one** of the three installation methods below. Most users should pick **Option 1**.

---

## Option 1️⃣ : One-Liner Installation (Recommended for Users)

### ✨ What It Does

- ✅ Automatically detects and installs Rust (if needed)
- ✅ Clones the full repository
- ✅ Builds the release binary
- ✅ Installs globally as `owpro` command
- ✅ Works from anywhere on your system

### 📥 Installation Command

```bash
curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh | bash
```

### ⏱️ Time Required
- **First run:** 10-15 minutes (includes Rust installation if needed)
- **Subsequent runs:** 2-5 minutes (updates only)

### ✅ After Installation

The script will:
1. Check for Rust and install if missing
2. Clone/update repository to `~/.local/share/omniwordlist-pro`
3. Build the release binary
4. Copy to `/usr/local/bin/owpro`
5. Show you quick start examples
6. Verify everything works

### 🎮 First Command After Install

```bash
owpro info
```

This shows your version and available features.

### 📋 Quick Commands

```bash
# Show version & features
owpro info

# List available presets
owpro list-presets

# Preview a preset (show 50 sample outputs)
owpro preview --preset pentest_default --sample-size 50

# Generate pentesting wordlist
owpro run --preset pentest_default -o pentest.txt

# Generate with custom charset (size 3-5)
owpro run --min 3 --max 5 --charset "abc" -o output.txt

# Generate with compression
owpro run --charset "abc123" --min 5 --max 10 --compress gzip -o wordlist.gz

# Browse available fields
owpro fields --categories

# Launch interactive TUI dashboard
owpro tui
```

---

## Option 2️⃣ : Quick Local Build (Recommended for Developers)

### ✨ What It Does

- ✅ Clone repository locally
- ✅ Build in your current directory
- ✅ Create shell alias for quick access
- ✅ Fast iteration for development
- ✅ No system-wide installation

### 🔧 Installation Commands

```bash
# Clone the repository
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git

# Navigate to project
cd OmniWordlistPro

# Run quick setup
./quick-install.sh
```

### ⏱️ Time Required
- **First run:** 5-8 minutes (builds from source)
- **Subsequent runs:** 1-2 minutes (incremental builds)

### ✅ After Installation

The script will:
1. Check for Rust installation
2. Build the release binary locally
3. Create `owpro` alias in your shell
4. Activate the alias immediately
5. Verify installation

### 🎮 Using After Setup

From the project directory:

```bash
owpro info
owpro run --min 3 --max 5 --charset abc
```

Or use the full path:

```bash
./target/release/omni run --min 3 --max 5 --charset abc
```

### 💡 Development Tips

```bash
# Build debug version (faster build, slower runtime)
cargo build

# Build release (slower build, faster runtime)
cargo build --release

# Run tests
cargo test

# Check for errors
cargo check

# Format code
cargo fmt

# Lint code
cargo clippy
```

---

## Option 3️⃣ : Manual Build (Full Control)

### ✨ What It Does

- ✅ Complete control over build process
- ✅ Use custom Rust flags and options
- ✅ Fine-tune compilation settings
- ✅ Perfect for advanced users

### 🔧 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro

# 2. Build release binary
cargo build --release

# 3. Verify build succeeded
./target/release/omni --version

# 4. Option A: Copy to /usr/local/bin (system-wide)
sudo cp target/release/omni /usr/local/bin/owpro
chmod +x /usr/local/bin/owpro

# 5. Option B: Add to PATH (no sudo needed)
echo 'export PATH="'$(pwd)'/target/release:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### ⏱️ Time Required
- **First run:** 5-10 minutes (full compilation)

### ✅ Verification

After installation, verify with:

```bash
owpro info                    # Should show version
owpro list-presets            # Should list presets
owpro --help                  # Should show CLI help
```

---

## 🔍 Troubleshooting & Common Issues

### Issue: "curl: command not found"

**Solution:** Install curl:
```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS
brew install curl

# CentOS/RHEL
sudo yum install curl
```

### Issue: "Rust not installed"

**Solution:** Install Rust manually:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Issue: "Permission denied" on /usr/local/bin

**Solution:** Use one of these:

```bash
# Option 1: Use sudo when copying
sudo cp target/release/omni /usr/local/bin/owpro

# Option 2: Use local installation (no sudo)
./quick-install.sh

# Option 3: Add to ~/.local/bin (user directory)
mkdir -p ~/.local/bin
cp target/release/omni ~/.local/bin/owpro
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "owpro: command not found" after install

**Solution:** Reload your shell:

```bash
# For bash
source ~/.bashrc

# For zsh
source ~/.zshrc

# Or open a new terminal window
```

### Issue: Build takes too long or fails

**Solution:** Try these steps:

```bash
# Clean previous build
cargo clean

# Check your connection (might be downloading dependencies)
cargo build --release --verbose

# If it still fails, check:
rustup update
cargo update
```

### Issue: "Build failed with error"

**Solution:** Check the error message and try:

```bash
# Update Rust
rustup update

# Clean and rebuild
cargo clean
cargo build --release --verbose

# If that fails, create an issue on GitHub
```

### Issue: Binary works but presets not found

**Solution:** Presets are included in the repository. They should be found automatically at:

```bash
# Preset location
~/.local/share/omniwordlist-pro/presets/

# Or in the source directory
./presets/
```

---

## 📊 System Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Rust** | 1.70+ | Auto-installed by Option 1 |
| **Git** | Any modern version | Required for cloning |
| **Disk Space** | 500 MB | For build artifacts |
| **RAM** | 2 GB minimum | 4+ GB recommended |
| **OS** | Linux, macOS, Windows | Works on all platforms |

### Supported Operating Systems

- ✅ Linux (Ubuntu, Debian, Fedora, CentOS, Arch, etc.)
- ✅ macOS (10.12+)
- ✅ Windows (with Git Bash or WSL2)

---

## 🎯 Common Workflows After Installation

### Workflow 1: Generate a Pentesting Wordlist

```bash
# Quick preview
owpro preview --preset pentest_default --sample-size 100

# Generate full wordlist
owpro run --preset pentest_default -o pentest.txt

# Generate compressed
owpro run --preset pentest_default --compress zstd -o pentest.txt.zst
```

### Workflow 2: Custom Charset Generation

```bash
# Simple: lowercase letters, 3-5 characters
owpro run --min 3 --max 5 --charset "abc" -o custom.txt

# Advanced: multiple charsets
owpro run --min 8 --max 12 \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789!@#" \
  -o advanced.txt

# With transformations
owpro run --min 8 --max 12 \
  --charset "abc123" \
  --prefix "user_" \
  --suffix "2024" \
  -o prefixed.txt
```

### Workflow 3: Field-Based Generation

```bash
# List all fields
owpro fields --categories

# List fields in category
owpro fields --category personal

# Generate from specific fields
owpro generate-fields \
  --fields first_name_male_0,last_name_0,common_suffix_0 \
  -o names.txt
```

### Workflow 4: Interactive Dashboard

```bash
# Launch the beautiful TUI interface
owpro tui

# Navigate using arrow keys
# Press 'h' or 'f1' for help
```

---

## 📚 Documentation Files

| File | Purpose | Best For |
|------|---------|----------|
| **README.md** | Full project documentation | Overview, features, examples |
| **QUICK_START.md** | Fast reference guide | Quick lookup of commands |
| **INSTALLATION.md** | Detailed installation | Deep dive into setup |
| **INSTALL.md** | This file - Comprehensive guide | Complete reference |

---

## 🔄 Updating OmniWordlist Pro

### Update via Option 1 (Easiest)

Just run the same command again:

```bash
curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh | bash
```

### Update via Option 2 (Local)

```bash
cd ~/path/to/OmniWordlistPro

# Pull latest changes
git pull origin main

# Rebuild
./quick-install.sh
```

### Update via Option 3 (Manual)

```bash
cd ~/path/to/OmniWordlistPro

# Pull latest changes
git pull origin main

# Rebuild release
cargo build --release

# Copy binary
sudo cp target/release/omni /usr/local/bin/owpro
```

---

## 🗑️ Uninstallation

### If installed via Option 1 (One-liner)

```bash
# Remove global command
sudo rm /usr/local/bin/owpro

# Remove cached repository (optional)
rm -rf ~/.local/share/omniwordlist-pro
```

### If installed via Option 2 (Local)

```bash
# Remove alias from shell config
# Edit ~/.bashrc or ~/.zshrc and remove the alias line

# Remove directory
rm -rf ~/path/to/OmniWordlistPro

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

### If installed via Option 3 (Manual)

```bash
# Remove global command
sudo rm /usr/local/bin/owpro

# Remove repository
rm -rf ~/path/to/OmniWordlistPro

# Remove from PATH (if added)
# Edit ~/.bashrc or ~/.zshrc and remove the PATH modification
```

---

## 📞 Getting Help

### Quick Help

```bash
# Show all commands
owpro --help

# Show specific command help
owpro run --help
owpro preview --help

# Show version info
owpro info
```

### Documentation

- **README.md** → Full feature documentation
- **QUICK_START.md** → Command reference
- **GitHub Repo** → https://github.com/AaryanBansal-dev/OmniWordlistPro

### Reporting Issues

```bash
# Create a bug report on GitHub
# https://github.com/AaryanBansal-dev/OmniWordlistPro/issues/new
```

---

## ✅ Installation Verification Checklist

After installation, verify everything works:

```bash
# ✓ Check version
owpro info

# ✓ List presets
owpro list-presets

# ✓ View help
owpro --help

# ✓ Generate sample
owpro preview --preset pentest_default --sample-size 10

# ✓ Generate file
owpro run --preset pentest_default --sample-size 100 -o test.txt

# ✓ Check file created
ls -lh test.txt
head test.txt
```

If all these commands succeed, you're ready to go! 🎉

---

## 💡 Tips & Best Practices

### Tip 1: Start with a Preview

Always preview before generating large wordlists:

```bash
owpro preview --preset your_preset --sample-size 1000
```

### Tip 2: Use Compression for Large Files

Save disk space with compression:

```bash
# ZSTD is fastest and best compression
owpro run --preset pentest_default --compress zstd -o wordlist.txt.zst

# GZIP is most compatible
owpro run --preset pentest_default --compress gzip -o wordlist.txt.gz
```

### Tip 3: Estimate Size Before Generating

Use the preview to understand what size you're creating:

```bash
owpro preview --preset pentest_default --sample-size 100
# Then calculate: sample × estimate = total size
```

### Tip 4: Keep a Development Build

Use Option 2 for a local development copy:

```bash
# Keep this for development and testing
cd ~/Projects/OmniWordlistPro
./quick-install.sh

# Keep your system install from Option 1
# in /usr/local/bin/owpro
```

### Tip 5: Use the TUI for Discovery

Launch the interactive dashboard to explore:

```bash
owpro tui
# Use arrow keys to navigate
# Browse presets, fields, and settings
```

---

## 🎓 Next Steps After Installation

1. **Run your first command:**
   ```bash
   owpro info
   ```

2. **Explore presets:**
   ```bash
   owpro list-presets
   owpro preview --preset pentest_default --sample-size 50
   ```

3. **Read the documentation:**
   - See `README.md` for features
   - See `QUICK_START.md` for command reference

4. **Generate your first wordlist:**
   ```bash
   owpro run --preset pentest_default -o my_wordlist.txt
   ```

5. **Try the interactive UI:**
   ```bash
   owpro tui
   ```

---

## 📋 Installation Quick Reference

| Method | Command | Time | Best For |
|--------|---------|------|----------|
| **One-Liner** | `curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh \| bash` | 10-15 min | Users, CI/CD |
| **Local Build** | `git clone https://...git && cd OmniWordlistPro && ./quick-install.sh` | 5-8 min | Developers |
| **Manual** | `git clone ... && cargo build --release && sudo cp...` | 5-10 min | Advanced users |

---

**Built with ❤️ in Rust** 🦀

For more information, visit: https://github.com/AaryanBansal-dev/OmniWordlistPro

---

*Last Updated: November 7, 2025*
