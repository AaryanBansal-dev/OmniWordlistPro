# 🚀 OmniWordlist Pro - Installation Guide Summary

## What We've Added

You now have **three simple ways** to install and use OmniWordlist Pro:

---

## ✨ Installation Methods

### 1️⃣ **One-Liner (Recommended for Users)**
```bash
curl -fsSL https://raw.githubusercontent.com/aaryan/omniwordlist-pro/main/install.sh | bash
```
- ✅ Works on Linux, macOS, Windows (with Git Bash)
- ✅ Handles Rust installation if needed
- ✅ Installs globally as `owpro` command
- ✅ Full automatic setup (5-10 minutes including Rust)

**Usage after install:**
```bash
owpro info
owpro list-presets
owpro preview --preset pentest_default --sample-size 50
```

---

### 2️⃣ **Quick Local Build (Recommended for Developers)**
```bash
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
./quick-install.sh
```
- ✅ Clones repo + builds locally
- ✅ Sets up `owpro` alias in your shell
- ✅ Fast iteration for development
- ✅ Works immediately after (5-8 minutes)

**Usage after install:**
```bash
owpro info
owpro run --min 3 --max 5 --charset abc -o out.txt
```

---

### 3️⃣ **Manual Build (Full Control)**
```bash
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
cargo build --release
sudo cp target/release/omni /usr/local/bin/owpro
```
- ✅ Complete control over build process
- ✅ Use custom Rust flags if needed
- ✅ Traditional install steps

---

## 📋 Files Created

### `install.sh` (Global Installation)
- **Purpose:** Automatic download, build, and global install
- **Target:** Users who want `owpro` available system-wide
- **Size:** 6.5 KB
- **Features:**
  - Automatic Rust installation
  - Git-based cloning to `~/.local/share/omniwordlist-pro`
  - Handles `sudo` gracefully
  - Colorized output with progress
  - Verification and help text

### `quick-install.sh` (Local Development)
- **Purpose:** Fast setup for developers working locally
- **Target:** Contributors and developers
- **Size:** 4.6 KB
- **Features:**
  - Local build and test
  - Shell alias setup
  - Works with bash/zsh
  - Live alias activation
  - No sudo required

### Updated `README.md`
- **New Section:** Installation (3 options with pros/cons)
- **Better formatting:** Clear icons, color-coded instructions
- **Verification steps:** How to test installation

---

## 🎯 Quick Start Examples

After installation, use `owpro` anywhere:

```bash
# Show version and features
owpro info

# List available presets
owpro list-presets

# Preview with sample size
owpro preview --preset pentest_default --sample-size 100

# Generate pentest wordlist
owpro run --preset pentest_default -o pentest.txt

# Generate with compression
owpro run --charset "abc123" --min 5 --max 10 --compress gzip -o wordlist.gz

# Browse fields
owpro fields --categories

# Launch TUI dashboard
owpro tui
```

---

## ✅ Installation Checklist

- [x] **install.sh** — Global automatic installer
  - [x] Rust detection/installation
  - [x] Git clone/pull logic
  - [x] Build orchestration
  - [x] Global PATH installation
  - [x] Verification
  - [x] Help text

- [x] **quick-install.sh** — Developer quick setup
  - [x] Local build
  - [x] Shell alias
  - [x] Immediate activation
  - [x] Verification
  - [x] Help text

- [x] **README.md** — Updated with 3 installation methods
  - [x] One-liner option
  - [x] Local build option
  - [x] Manual build option
  - [x] Verification instructions

---

## 🔍 How They Work

### `install.sh` Flow
```
User runs: curl ... | bash
    ↓
Check Rust → Install if missing
    ↓
Clone repo to ~/.local/share/omniwordlist-pro
    ↓
cargo build --release
    ↓
cp binary → /usr/local/bin/owpro (with sudo if needed)
    ↓
Verify: owpro --version works
    ↓
Show help & examples
```

### `quick-install.sh` Flow
```
User runs: ./quick-install.sh (from repo root)
    ↓
Check Cargo.toml exists
    ↓
Verify Rust installed
    ↓
cargo build --release
    ↓
Add alias owpro to ~/.bashrc/.zshrc
    ↓
Activate alias immediately
    ↓
Verify installation
    ↓
Show help & examples
```

---

## 📝 Usage After Installation

### For Users (installed via install.sh)
```bash
# Use owpro command globally
owpro preview --preset pentest_default --sample-size 50
owpro run --preset pentest_default -o output.txt
```

### For Developers (installed via quick-install.sh)
```bash
# In the project directory
owpro run --min 3 --max 5 --charset abc
# Or use full path
./target/release/omni run --min 3 --max 5 --charset abc
```

---

## 🛠️ Troubleshooting

### Issue: "Rust not installed"
**Solution:** `install.sh` handles this automatically. If manual:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Issue: "Permission denied" for /usr/local/bin
**Solution:** `install.sh` uses `sudo` with prompts. Or use local build.

### Issue: "owpro: command not found" after quick-install.sh
**Solution:** Reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Issue: Build timeout or failure
**Solution:** Rebuild with more verbosity:
```bash
cargo build --release --verbose
```

---

## 🚀 Next Steps

1. **Test Global Install:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/aaryan/omniwordlist-pro/main/install.sh | bash
   ```

2. **Or Test Local Build:**
   ```bash
   git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
   cd OmniWordlistPro
   ./quick-install.sh
   ```

3. **Verify:**
   ```bash
   owpro info
   ```

4. **Generate Your First Wordlist:**
   ```bash
   owpro run --preset pentest_default --sample-size 100
   ```

---

## 📊 System Requirements

| Method | OS | Rust | Git | Time |
|--------|----|----|-----|------|
| **One-liner** | Linux/macOS/Windows | Auto-install | Required | 10-15 min (first time) |
| **Quick Local** | Linux/macOS/Windows | Required | Required | 5-8 min |
| **Manual** | Linux/macOS/Windows | Required | Required | 5-10 min |

---

## 💡 Tips

- **For CI/CD:** Use `install.sh` for reproducible builds
- **For Development:** Use `quick-install.sh` for fast iteration
- **For Containers:** Copy `Dockerfile` example (if needed):
  ```dockerfile
  FROM rust:latest
  WORKDIR /app
  COPY . .
  RUN cargo build --release
  RUN cp target/release/omni /usr/local/bin/owpro
  ENTRYPOINT ["owpro"]
  ```

---

## 📞 Support

- **GitHub Issues:** Report bugs
- **GitHub Discussions:** Ask questions
- **Documentation:** See README.md for full CLI reference

---

**Built with ❤️ in Rust** 🦀
