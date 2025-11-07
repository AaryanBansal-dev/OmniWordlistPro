# Installation Scripts Guide

## Overview

OmniWordlist Pro provides **three installation scripts** with different levels of detail and progress feedback:

| Script | Best For | Progress Detail | Time Estimate |
|--------|----------|-----------------|----------------|
| **quick-install.sh** | Local development & testing | Moderate - shows crate compilation | ~5-15 min |
| **install.sh** | System-wide installation | Moderate - shows all steps | ~5-15 min |
| **install-verbose.sh** | Troubleshooting builds | Full detail - real-time crate tracking | ~5-15 min |

---

## Understanding the Build Process

### Why does the first build take so long?

The first build takes **5-15 minutes** because:

1. **Dependency Downloads** — ~50 Rust crates are downloaded from crates.io
2. **Compilation** — Each crate is compiled from source code to machine code
3. **Linking** — All compiled crates are linked together into a single binary
4. **Optimization** — Release mode applies heavy optimizations (makes binary faster but takes longer)

**Subsequent builds are faster** (~1-2 minutes) because:
- Cargo caches already-compiled dependencies
- Only changed code is recompiled
- Incremental compilation picks up where it left off

### Why the old script looked frozen

The old script used:
```bash
cargo build --release
```

Without any special flags, this command:
- ❌ Shows nothing until it finishes
- ❌ Provides no progress feedback
- ❌ No way to tell if it's still working or hung
- ❌ Users would think it froze or crashed

---

## Installation Methods

### Option 1: Quick Local Build (Recommended for Development)

**Use this if:** You want to build and test locally

```bash
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
./quick-install.sh
```

**What it does:**
- ✅ Shows each crate being compiled
- ✅ Sets up local alias (`owpro`)
- ✅ No system-wide installation
- ✅ Fast startup
- ✅ Best for developers

**Progress shows:**
```
▶ Building OmniWordlist Pro (release mode)...
📦 First build takes 5-15 minutes (compiling dependencies)
💡 Watching compilation progress:

  ⚙️  Compiling tokio
  ⚙️  Compiling regex
  ⚙️  Compiling serde
  🔗 dependency resolved
  (3 crates compiled in 15s)
  ...
✓ Build completed!
```

### Option 2: System-Wide Installation

**Use this if:** You want to use `owpro` from anywhere on your system

```bash
./install.sh
```

**What it does:**
- ✅ Downloads from GitHub (or updates if already present)
- ✅ Builds the binary
- ✅ Installs to `/usr/local/bin/owpro`
- ✅ Shows compilation progress
- ✅ Verifies installation

**Result:** You can use `owpro` from any terminal:
```bash
owpro list-presets
owpro run --preset pentest_default -o wordlist.txt
```

### Option 3: Verbose Build Troubleshooting

**Use this if:** Build seems stuck or you want maximum detail

```bash
./install-verbose.sh
```

**What it does:**
- ✅ Shows **every** crate being compiled
- ✅ Displays download progress
- ✅ Shows compilation timing
- ✅ Displays crate counts every 5 crates
- ✅ Best for diagnosing build issues

**Progress shows:**
```
⚙️  Compiling: tokio
⚙️  Compiling: regex
  (5 crates compiled in 45s)
⚙️  Compiling: serde
⚙️  Compiling: serde_json
⚙️  Compiling: clap
  (10 crates compiled in 90s)
...
✓ Build completed in 420 seconds!
  Compiled 52 crates
✓ Binary created: target/release/omni (8.2M)
```

---

## Real Build Progress Examples

### First-time build (fresh clone):
```
Resolving dependencies...
Downloading ahash...
Downloading regex...
⚙️  Compiling: ahash
⚙️  Compiling: bytemuck
⚙️  Compiling: serde
⚙️  Compiling: tokio
... [many more crates] ...
⚙️  Compiling: omniwordlist-pro
🔗 Linking binary...
✓ Build completed!
Total: 52 crates in 420 seconds
```

### Second build (after changes):
```
⚙️  Compiling: omniwordlist-pro (changed files only)
🔗 Linking binary...
✓ Build completed in 45 seconds
```

---

## What Each Script Shows

### quick-install.sh Output
```
🦀 OmniWordlist Pro - Quick Local Setup

▶ Checking Rust toolchain...
✓ Rust is ready (rustc 1.70.0)

▶ Building OmniWordlist Pro (release mode)...
📦 First build takes 5-15 minutes (compiling dependencies)
💡 Watching compilation progress:

  ⚙️  Compiling ahash
  ⚙️  Compiling bytemuck
  ⚙️  Compiling num-traits
  [... more crates ...]
  ⚙️  Compiling omniwordlist-pro

✓ Build completed!
✓ Binary ready at: ./target/release/omni
✓ Added alias to ~/.bashrc
✓ Alias is active now!

═══════════════════════════════════════════════════════
Setup Complete! 🎉
═══════════════════════════════════════════════════════

You can now use:
  owpro info
  owpro list-presets
  owpro preview --preset pentest_default
  owpro run --min 3 --max 5 --charset abc
```

### install.sh Output
```
╔═══════════════════════════════════════════════════════════╗
║  🦀 OmniWordlist Pro - Installation Script         ║
╚═══════════════════════════════════════════════════════════╝

▶ Checking prerequisites...
✓ Rust is installed (1.70.0)

▶ Cloning/updating repository...
✓ Repository ready at: /home/user/.local/share/omniwordlist-pro

▶ Building binary (release mode)...
📦 First build takes 5-15 minutes
💡 You'll see crates being compiled below:

  ⚙️  ahash
  ⚙️  tokio
  ⚙️  regex
  [... compiling ...]
✓ Binary built successfully!

▶ Installing globally...
✓ Installed to /usr/local/bin/owpro (no sudo needed)

▶ Verifying installation...
✓ Installation verified!

═══════════════════════════════════════════════════════
Installation Complete! 🎉
═══════════════════════════════════════════════════════
```

### install-verbose.sh Output
```
🦀 OmniWordlist Pro - Verbose Installation Script

▶ Checking Rust installation...
✓ Rust is installed: rustc 1.70.0 (stable-x86_64-unknown-linux-gnu)
  └─ Cargo: cargo 1.70.0

▶ Setting up repository...
ℹ Cloning repository...
✓ Repository ready at: /home/user/.local/share/omniwordlist-pro

▶ Building OmniWordlist Pro (Release Mode)

This may take 5-15 minutes on first build
(Dependencies are compiled once, subsequent builds are faster)

Compilation Progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔗 Resolving dependencies...
  ↓ Downloading: ahash 0.8
  ⚙️  Compiling: ahash
  ⚙️  Compiling: bytemuck
  ⚙️  Compiling: num-traits
  ⚙️  Compiling: typenum
  ⚙️  Compiling: generic-array
     (5 crates compiled in 45s)
  ⚙️  Compiling: serde
  ⚙️  Compiling: indexmap
  ⚙️  Compiling: itoa
  ⚙️  Compiling: ryu
  ⚙️  Compiling: serde_json
     (10 crates compiled in 95s)
  [... continues showing progress ...]
  ⚙️  Compiling: omniwordlist-pro
  🔗 Linking binary...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Build completed in 420 seconds!
  └─ Compiled 52 crates
✓ Binary created: target/release/omni (8.2M)
```

---

## Troubleshooting Build Issues

### Problem: Build seems stuck or frozen

**Solution:** This is normal on first build! 

- ✅ First build: 5-15 minutes (compiling all dependencies)
- ✅ Use `install-verbose.sh` to see exact progress
- ✅ Press `Ctrl+C` safely to cancel (doesn't corrupt anything)

### Problem: Out of disk space

**Solution:** Build needs ~5-10 GB temporary space

```bash
# Check available space
df -h

# Clean old builds if needed
cargo clean
```

### Problem: Build fails with "error: linker `cc` not found"

**Solution:** Install build tools

```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf groupinstall "Development Tools"

# macOS
xcode-select --install
```

### Problem: "command not found: cargo"

**Solution:** Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

---

## Performance Tips

### Make subsequent builds faster:

1. **Use debug builds during development:**
   ```bash
   cargo build          # Much faster than --release
   ./target/debug/omni  # Use debug binary for testing
   ```

2. **Use incremental compilation:**
   ```bash
   CARGO_INCREMENTAL=1 cargo build --release
   ```

3. **Use more CPU cores (if available):**
   ```bash
   cargo build --release -j 8  # Use 8 cores instead of auto
   ```

4. **View actual progress in real-time:**
   ```bash
   cargo build --release -v 2>&1 | grep "Compiling\|Finished"
   ```

---

## Next Steps After Installation

### Verify it works:
```bash
owpro info                           # Check version
owpro list-presets                   # See available presets
owpro preview --preset pentest_default --sample-size 10
```

### Try some commands:
```bash
# Basic generation
owpro run --min 3 --max 5 --charset abc -o test.txt
cat test.txt

# With preset
owpro run --preset pentest_default -o pentest.txt --sample-size 100

# Compressed output
owpro run --charset "abc123" --min 5 --max 10 --compress gzip -o words.gz
```

### Interactive mode:
```bash
owpro tui                            # Launch the TUI (experimental)
```

---

## Script Files

- **`quick-install.sh`** — Fast local setup (best for dev)
- **`install.sh`** — System-wide installation (best for users)
- **`install-verbose.sh`** — Detailed troubleshooting (best for debugging)

All scripts are **idempotent** — safe to run multiple times without issues.

---

## Questions?

- 📚 See **INSTALL.md** for more detailed installation info
- 📚 See **QUICK_START.md** for command reference
- 📚 See **README.md** for project overview
- 💬 Report issues: https://github.com/AaryanBansal-dev/OmniWordlistPro/issues
