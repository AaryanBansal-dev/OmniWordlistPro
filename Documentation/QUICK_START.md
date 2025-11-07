# 📖 Quick Start & Command Reference

**Version:** 1.1.0  
**Tested on:** macOS, Linux (Ubuntu, Fedora)

---

## Installation (30 seconds)

```bash
# Clone and build
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro
cargo build --release

# Create alias for easier access
alias omni="$(pwd)/target/release/omni"

# Verify
omni info
```

See [INSTALL.md](INSTALL.md) for detailed installation guide.

---

## Getting Help

```bash
# Show all commands
omni --help

# Show command-specific help
omni run --help
omni preview --help

# Show version & system info
omni info
```

---

## Core Commands

### `omni run` — Generate a wordlist

**Basic usage:**
```bash
# Simple generation
omni run --min 3 --max 5 --charset "abc" -o output.txt

# Check the output
cat output.txt
# aaa, aab, aac, aba, abb, ...
```

**With prefix/suffix:**
```bash
omni run --min 5 --max 10 \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  --prefix "user_" \
  --suffix "!2024" \
  -o output.txt
```

**With compression:**
```bash
# GZIP (most compatible)
omni run --min 6 --max 8 --charset abc \
  --compress gzip -o output.txt.gz

# ZSTD (fastest)
omni run --min 6 --max 8 --charset abc \
  --compress zstd -o output.txt.zst

# BZIP2 (best ratio)
omni run --min 6 --max 8 --charset abc \
  --compress bzip2 -o output.txt.bz2
```

**Using presets:**
```bash
# Generate from preset
omni run --preset pentest_default -o pentest.txt

# Generate 100 samples from preset
omni run --preset pentest_default -s 100 -o sample.txt
```

**With different output formats:**
```bash
# JSONL (one JSON per line)
omni run --min 3 --max 5 --charset abc \
  --format jsonl -o output.jsonl

# CSV format
omni run --min 3 --max 5 --charset abc \
  --format csv -o output.csv
```

**All `run` options:**
```
--min <LEN>              Minimum word length
--max <LEN>              Maximum word length
--charset <STR>         Character set to use
--prefix <STR>          Prepend to each token
--suffix <STR>          Append to each token
--preset <NAME>         Use preset configuration
--compress <FORMAT>     Compression (gzip, bzip2, lz4, zstd)
--format <FMT>          Output format (txt, jsonl, csv)
-o, --output <FILE>     Output file path
-s, --sample-size <N>   Limit to N tokens
```

---

### `omni preview` — Preview before generating

```bash
# Preview a preset
omni preview --preset pentest_default --sample-size 50

# Preview custom generation
omni preview --min 5 --max 10 --charset "abc123" --sample-size 20

# Show first 10 (default)
omni preview --preset pentest_default
```

**Output shows:**
- Sample tokens
- Generation stats
- Quality information

---

### `omni list-presets` — Show available presets

```bash
# List all presets
omni list-presets

# Output:
# Available Presets:
# 1. pentest_default       - Standard pentesting wordlist
# 2. meme_humor_pack       - Creative with humor
# 3. api_dev_wordlist      - API endpoint patterns
# 4. social_media_usernames - Social handles
# 5. pattern_basic         - Crunch-style patterns
```

---

### `omni show-preset` — Show preset details

```bash
# Display full preset configuration
omni show-preset pentest_default

# Shows:
# Name: pentest_default
# Description: Standard pentesting wordlist
# Min length: 8
# Max length: 16
# Charset: ...
# Transforms: [...]
```

---

### `omni fields` — Browse available fields

```bash
# List all field categories
omni fields --categories

# Output:
# Available Categories:
# - personal
# - technical
# - humor
# - language
# - business
# - keyboard
# - etc.

# List fields in a category
omni fields --category personal

# Search for fields
omni fields --search keyboard
```

---

### `omni info` — Show version & features

```bash
omni info

# Output shows:
# OmniWordlist Pro v1.1.0
# Rust 1.75.0
# Available transforms: 100+
# Supported formats: TXT, JSONL, CSV
# Compression: GZIP, BZIP2, LZ4, ZSTD
```

---

### `omni tui` — Interactive dashboard (Experimental)

```bash
# Launch interactive UI
omni tui

# Use arrow keys to navigate
# Press ? for help
# Press q to quit
```

Features:
- Browse presets
- Explore fields
- Configure generation
- Real-time previews

---

## Common Workflows

### Workflow 1: Quick Test

```bash
# Test basic functionality
omni run --min 2 --max 3 --charset "ab" -o test.txt
cat test.txt

# Expected: a, b, aa, ab, ba, bb
```

### Workflow 2: Pentesting Wordlist

```bash
# Preview first
omni preview --preset pentest_default --sample-size 100

# Generate full wordlist
omni run --preset pentest_default -o pentest.txt

# Check size
wc -l pentest.txt
du -h pentest.txt

# Compress if large
gzip pentest.txt
```

### Workflow 3: Custom Charset

```bash
# Lowercase only, 5-8 chars
omni run \
  --min 5 --max 8 \
  --charset "abcdefghijklmnopqrstuvwxyz" \
  -o wordlist.txt

# Lowercase + digits, 6-10 chars
omni run \
  --min 6 --max 10 \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  -o wordlist.txt

# All characters, 8-12 chars
omni run \
  --min 8 --max 12 \
  --charset "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()" \
  -o wordlist.txt
```

### Workflow 4: Pattern-based (Crunch-style)

```bash
# Patterns: @ = lowercase, % = digit, ^ = symbol, , = uppercase
# Example: pass%% generates: pass00, pass01, ..., pass99

omni run \
  --pattern "pass%%" \
  --min 6 --max 6 \
  -o passwords.txt

# With custom charset for pattern
omni run \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  --min 5 --max 10 \
  -o wordlist.txt
```

### Workflow 5: Compression Comparison

```bash
# Generate same data with different compression
omni run --min 6 --max 8 --charset abc -o output.txt
omni run --min 6 --max 8 --charset abc --compress gzip -o output.gz
omni run --min 6 --max 8 --charset abc --compress zstd -o output.zst
omni run --min 6 --max 8 --charset abc --compress bzip2 -o output.bz2

# Compare sizes
ls -lh output* | awk '{print $5, $9}'

# GZIP: ~60% of original
# ZSTD: ~50% of original  
# BZIP2: ~45% of original
```

### Workflow 6: JSON Export

```bash
# Generate as JSONL
omni run \
  --min 4 --max 6 \
  --charset "abc123" \
  --format jsonl \
  -o output.jsonl

# View the data
head -5 output.jsonl
```

---

## Character Set Examples

### Predefined Sets

```bash
# Lowercase letters
--charset "abcdefghijklmnopqrstuvwxyz"

# Uppercase letters
--charset "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Digits
--charset "0123456789"

# Common special characters
--charset "!@#$%^&*()"

# Hex characters
--charset "0123456789abcdef"

# Custom combination
--charset "abc123!@#"
```

### Using Patterns

```bash
# @ = lowercase, % = digits, ^ = symbols, , = uppercase
omni run --pattern "password@@@%%%"    # password + 3 lowercase + 3 digits

# Common patterns
omni run --pattern "admin%%"           # admin + 2 digits
omni run --pattern "test@@@@"          # test + 4 lowercase
omni run --pattern "user^"             # user + 1 symbol
```

---

## Output Examples

### TXT Format (Default)

```
aaa
aab
aac
aba
abb
```

### JSONL Format

```json
{"token":"aaa","length":3}
{"token":"aab","length":3}
{"token":"aac","length":3}
```

### CSV Format

```
token,length
aaa,3
aab,3
aac,3
```

---

## Tips & Tricks

### Tip 1: Always Preview First

```bash
# Preview sample before full generation
omni preview --preset pentest_default --sample-size 1000

# This helps estimate final size and output quality
```

### Tip 2: Use Compression

```bash
# Saves 50-70% disk space
omni run --preset pentest_default --compress zstd -o wordlist.txt.zst

# Decompress when needed
zstd -d wordlist.txt.zst
```

### Tip 3: Create an Alias

```bash
# Add to ~/.bashrc
alias omni="$(pwd)/target/release/omni"

# Or for system-wide
sudo cp target/release/omni /usr/local/bin/
```

### Tip 4: Count Lines

```bash
# Check how many tokens generated
wc -l output.txt

# Or with compression
zcat output.txt.gz | wc -l
zstd -d -c output.txt.zst | wc -l
```

### Tip 5: View Sample

```bash
# Show first 10 lines
head output.txt

# Show last 10 lines
tail output.txt

# Show random 10 lines
shuf output.txt | head -10

# Count unique tokens
sort output.txt | uniq | wc -l
```

---

## Common Issues

### Issue: "command not found: omni"

**Solution:** Create alias or use full path:

```bash
alias omni="$(pwd)/target/release/omni"
# or
./target/release/omni info
```

### Issue: Output file very large

**Solution:** Use compression or limit output:

```bash
# Compress output
omni run --charset abc --min 6 --max 8 --compress zstd -o output.zst

# Or limit to sample
omni run --charset abc --min 6 --max 8 -s 100000 -o sample.txt
```

### Issue: Generation takes too long

**Solution:** Reduce charset or max length:

```bash
# Smaller charset
omni run --charset "abc" --min 5 --max 8 -o output.txt

# Shorter max length
omni run --charset abc --min 3 --max 5 -o output.txt
```

---

## See Also

- **[README.md](README.md)** — Full documentation & features
- **[INSTALL.md](INSTALL.md)** — Installation guide
- **[DEVELOPMENT.md](DEVELOPMENT.md)** — Development guide
- **[FEATURES.md](FEATURES.md)** — Feature list & status

---

**Built with ❤️ in Rust** 🦀
