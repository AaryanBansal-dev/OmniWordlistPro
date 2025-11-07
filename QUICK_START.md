# ✅ Installation Complete - Quick Reference

## 🎯 You Now Have 3 Ways to Install & Use OmniWordlist Pro

---

## 1️⃣ **Global Install (Easiest)**

```bash
curl -fsSL https://raw.githubusercontent.com/aaryan/omniwordlist-pro/main/install.sh | bash
```

**Then use anywhere:**
```bash
owpro info
owpro preview --preset pentest_default --sample-size 50
```

---

## 2️⃣ **Local Development Install**

```bash
git clone https://github.com/aaryan/omniwordlist-pro.git
cd omniwordlist-pro
./quick-install.sh
```

**Then use:**
```bash
owpro run --min 3 --max 5 --charset abc -o output.txt
```

---

## 3️⃣ **Manual Build**

```bash
cargo build --release
sudo cp target/release/omni /usr/local/bin/owpro
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Full documentation, features, CLI reference |
| **INSTALLATION.md** | Detailed installation guide and troubleshooting |
| **install.sh** | Automatic global installer (for GitHub) |
| **quick-install.sh** | Developer quick setup script |

---

## 🚀 Quick Start

```bash
# After installing, try these commands:

owpro info                                          # Show version

owpro list-presets                                  # List presets

owpro preview --preset pentest_default              # Preview preset

owpro run --min 3 --max 5 --charset abc -o out.txt  # Generate

owpro fields --categories                           # Browse fields

owpro tui                                           # Launch dashboard
```

---

## ✨ What Each Script Does

### **install.sh** (for global use)
- ✅ Installs Rust if missing
- ✅ Clones repo to `~/.local/share/omniwordlist-pro`
- ✅ Builds release binary
- ✅ Copies to `/usr/local/bin/owpro` (with sudo)
- ✅ Makes `owpro` available system-wide

### **quick-install.sh** (for development)
- ✅ Checks Rust is installed
- ✅ Builds release binary locally
- ✅ Adds `owpro` alias to shell
- ✅ Activates immediately (no shell reload needed)
- ✅ Works in project directory

---

## 📋 What's Included

### Binary (`omni`)
- Compiled Rust application
- Full wordlist generation engine
- 1500+ fields supported
- 100+ transforms available
- Beautiful TUI interface
- Multiple compression formats

### 5 Built-in Presets
1. **pentest_default** — Penetration testing wordlist
2. **meme_humor_pack** — Creative with emojis
3. **api_dev_wordlist** — API endpoint patterns
4. **social_media_usernames** — Social handles
5. **pattern_basic** — Simple Crunch patterns

### Features
- ✅ Crunch-compatible patterns (@, %, ^, ,)
- ✅ Field-based generation
- ✅ Leet, homoglyph, emoji transforms
- ✅ Entropy & quality filtering
- ✅ GZIP, BZIP2, LZ4, ZSTD compression
- ✅ Checkpointing & resume
- ✅ Deduplication
- ✅ JSONL & CSV export

---

## 🎓 Common Workflows

### Generate a Pentesting Wordlist
```bash
owpro run --preset pentest_default -o pentest.txt
```

### Generate with Custom Charset
```bash
owpro run --min 8 --max 16 --charset "abc123" -o custom.txt
```

### Generate with Compression
```bash
owpro run --preset pentest_default --compress gzip -o output.txt.gz
```

### Preview Before Generating
```bash
owpro preview --preset pentest_default --sample-size 1000
```

### Export Preset as JSON
```bash
owpro export-preset pentest_default --format json -o my_preset.json
```

### List All Available Fields
```bash
owpro fields --categories
```

### Use Interactive Dashboard
```bash
owpro tui
```

---

## 🔧 Troubleshooting

### Command not found
```bash
# Reload shell after install
source ~/.bashrc  # or ~/.zshrc
```

### Permission denied
```bash
# Use sudo for /usr/local/bin or use local install
./quick-install.sh
```

### Build too slow
```bash
# Check internet, Rust may be downloading dependencies
# First build takes longer (5-8 min typical)
```

---

## 📞 Need Help?

- **README.md** → Full documentation
- **INSTALLATION.md** → Detailed installation guide
- **GitHub Issues** → Report bugs
- **GitHub Discussions** → Ask questions

---

## 🎉 You're Ready!

Pick an installation method and run one of the quick start commands.

**Recommended first command:**
```bash
owpro info
```

This shows you the version and available features.

---

**Built with ❤️ in Rust** 🦀
