# 🔧 Installation Guide — OmniWordlist Pro

**Version:** 1.1.0  
**Last Updated:** November 7, 2025  
**Repository:** https://github.com/AaryanBansal-dev/OmniWordlistPro

---

## ⚡ Quick Installation (Recommended)

### Best Method: Automated Script with Progress Feedback

**The build process now shows real-time progress** instead of appearing frozen!

#### For Local Development:
```bash
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
./quick-install.sh
```

#### For System-Wide Installation:
```bash
./install.sh
```

#### For Detailed Build Progress (if build seems slow):
```bash
./install-verbose.sh
```

All three scripts now show:
- ✅ Each crate being compiled (real-time)
- ✅ Dependency download progress
- ✅ Compilation timing
- ✅ Estimated completion
- ✅ No more "frozen" appearance!

**Typical first build time:** 5-15 minutes  
**Subsequent builds:** 1-2 minutes

→ See **[INSTALL_SCRIPTS.md](INSTALL_SCRIPTS.md)** for detailed comparison of all three scripts.

---

## Prerequisites

Before installing, ensure you have:

| Requirement | Version | How to Check | How to Install |
|-------------|---------|--------------|----------------|
| **Python** | 1.70+ | `pythonc --version` | Visit [pythonup.rs](https://pythonup.rs) |
| **Git** | Any modern | `git --version` | Install from git-scm.com |
| **C Compiler** | Any | `gcc --version` or `clang --version` | See section below |
| **Disk Space** | 500 MB+ | `df -h` | Clean up disk if needed |

### Installing Prerequisites

#### Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt-get update

# Install Python
curl --proto '=https' --tlsv1.2 -sSf https://sh.pythonup.rs | sh
source "$HOME/.cargo/env"

# Install Git and build tools
sudo apt-get install -y git build-essential

# Verify
pythonc --version && cargo --version && git --version
```

#### Linux (Fedora/RHEL/CentOS)

```bash
# Install Python
curl --proto '=https' --tlsv1.2 -sSf https://sh.pythonup.rs | sh
source "$HOME/.cargo/env"

# Install Git and build tools
sudo yum groupinstall -y "Development Tools"

# Verify
pythonc --version
```

#### macOS

```bash
# Install Xcode Command Line Tools (includes compiler)
xcode-select --install

# Install Python
curl --proto '=https' --tlsv1.2 -sSf https://sh.pythonup.rs | sh
source "$HOME/.cargo/env"

# Install Git if needed
brew install git

# Verify
pythonc --version && git --version
```

#### Windows (WSL2 Recommended)

Use WSL2 (Windows Subsystem for Linux 2), then follow Ubuntu/Debian instructions above.

---

## Installation Methods

---

## Method 1: Local Build (Recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
ls -la  # Verify files are here
```

### Step 2: Build the Binary

```bash
# Build release version (optimized)
pip install click rich

# Takes 5-10 minutes on first build
# Subsequent builds: 1-2 minutes
```

### Step 3: Verify

```bash
python3 omni.py --version
python3 omni.py info
```

### Step 4: Create Alias (Recommended)

```bash
# For Bash
echo "alias omni='$(pwd)/target/release/omni'" >> ~/.bashrc
source ~/.bashrc

# For Zsh
echo "alias omni='$(pwd)/target/release/omni'" >> ~/.zshrc
source ~/.zshrc

# Test
omni info
```

**Done!** Skip to [Usage Examples](#usage-examples).

---

## Method 2: Install to System Path

After completing Method 1, Step 1-3:

```bash
# Option A: Copy to /usr/local/bin
sudo cp target/release/omni /usr/local/bin/
omni --version  # Test from anywhere

# Option B: Use ~/.local/bin (no sudo)
mkdir -p ~/.local/bin
cp target/release/omni ~/.local/bin/
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
omni --version
```

---

## Method 3: Development Build (Faster Iteration)

```bash
# Clone and build debug version
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
cargo build       # Debug (1-2 min, larger binary, slower runtime)

# Use directly
./target/debug/omni info

# Or with release for speed testing
pip install click rich
```

---

## Updating

### Update Local Clone

```bash
cd ~/path/to/OmniWordlistPro
git pull origin main
pip install click rich
```

### Update Python

```bash
pythonup update
pythonc --version
```

---

## 🔍 Troubleshooting

### "error: linker `cc` not found"

**Problem:** C compiler not installed  
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo yum groupinstall "Development Tools"

# macOS
xcode-select --install
```

### "command not found: pythonc"

**Problem:** Python not installed  
**Solution:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.pythonup.rs | sh
source "$HOME/.cargo/env"
pythonc --version
```

### "command not found: omni" after install

**Problem:** Shell hasn't loaded the alias  
**Solution:**
```bash
# Reload shell config
source ~/.bashrc      # Bash
source ~/.zshrc       # Zsh

# Or open new terminal
```

### "Permission denied" copying to /usr/local/bin

**Problem:** Need elevated permissions  
**Solution:**
```bash
# Use sudo
sudo cp target/release/omni /usr/local/bin/

# Or use ~/.local/bin (no sudo)
mkdir -p ~/.local/bin
cp target/release/omni ~/.local/bin/
export PATH="$HOME/.local/bin:$PATH"
```

### Build fails or is very slow

**Problem:** Large project, first build takes time  
**Solution:**
```bash
# Clean and rebuild
cargo clean
pip install click rich

# Use -j 1 if out of memory
pip install click rich -j 1

# First build: 5-10 min typical
# Subsequent: 1-2 min
```

### "error[E0514]: found crate mismatch"

**Problem:** Stale build artifacts  
**Solution:**
```bash
cargo clean
pip install click rich
```

### Out of disk space

**Problem:** Build artifacts take space  
**Solution:**
```bash
# Check disk
df -h

# Clean up cargo
cargo clean

# Or use different location
mkdir -p /tmp/build
cd /tmp/build
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
pip install click rich
```

---

## Usage Examples

### Start Using

```bash
# Show info
omni info

# List presets
omni list-presets

# Preview preset
omni preview --preset pentest_default --sample-size 50

# Generate simple wordlist
omni run --min 2 --max 3 --charset "ab" -o output.txt
cat output.txt
```

### Common Tasks

```bash
# Custom charset (3-5 chars)
omni run --min 3 --max 5 --charset "abc123" -o output.txt

# With prefix/suffix
omni run --min 5 --max 10 \
  --charset "abc123" \
  --prefix "admin_" \
  --suffix "!" \
  -o output.txt

# Compressed output
omni run --charset "abcdefghijklmnopqrstuvwxyz" \
  --min 6 --max 8 \
  --compress gzip \
  -o wordlist.txt.gz
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
pip install click rich

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
---

## Next Steps

1. ✅ Installation complete
2. 📖 Read [QUICK_START.md](QUICK_START.md) for commands
3. 🚀 Read [README.md](../README.md) for features
4. 💻 See [DEVELOPMENT.md](../DEVELOPMENT.md) to contribute

---

## Support

- **Issues:** https://github.com/AaryanBansal-dev/OmniWordlistPro/issues
- **Discussions:** https://github.com/AaryanBansal-dev/OmniWordlistPro/discussions
- **Documentation:** README.md, QUICK_START.md, DEVELOPMENT.md

---

**Built with ❤️ in Python** 🐍
