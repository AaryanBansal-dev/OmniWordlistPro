# OmniWordlist Pro — Python Edition

**Version:** 1.1.0  
**Author:** Aaryan Bansal  
**Language:** 100% Pure Python 🐍  
**Original Python Version:** [https://github.com/AaryanBansal-dev/OmniWordlistPro](https://github.com/AaryanBansal-dev/OmniWordlistPro)  
**Status:** ✅ Actively Maintained  

---

## Overview

This is a **complete Python rewrite** of OmniWordlist Pro, maintaining full functionality from the original Python implementation. The Python version provides an accessible, easy-to-install alternative while preserving all the enterprise features of the original.

**OmniWordlist Pro** is a **production-ready, ultra-high-performance wordlist generation platform**. It combines:

- ✅ **Crunch compatibility**: Pattern-based generation with charset support (@, %, ^, ,)
- ✅ **CUPP integration**: 1500+ toggleable fields for personalization
- ✅ **17+ transforms**: Leet, homoglyph, emoji, phonetic, keyboard shifts, etc.
- ✅ **Enterprise features**: Checkpointing, deduplication, compression
- ✅ **Beautiful CLI**: Rich-based interface with colors and progress bars
- ✅ **Streaming architecture**: Memory-efficient, no OOM on massive lists
- ✅ **Multi-format output**: TXT, GZIP, BZIP2, LZ4, ZSTD, JSONL, CSV

Perfect for:
- 🎯 Penetration testers & red teams
- 🎯 Bug bounty hunters
- 🎯 Security researchers
- 🎯 Credential auditing

---

## 🚀 Quick Install & Run

### Prerequisites
- **Python 3.8+** (install from [python.org](https://python.org))
- **pip** (comes with Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro

# Install the package
pip install -e .

# Verify installation
omni --version
omni info
```

### First Test

```bash
# Generate a quick wordlist
omni run --min 3 --max 3 --charset abc -o test.txt --sample-size 10

# Preview a preset
omni preview --preset pentest_default --sample-size 20

# List all available presets
omni list-presets
```

---

## Core Features

### 🎯 Generation & Combinatorics
- ✅ **Charset-based generation** — Custom character sets with Crunch-style patterns
- ✅ **Pattern support** — `@` (lower), `%` (digit), `^` (symbol), `,` (upper) expansion
- ✅ **Length constraints** — Min/max word length control
- ✅ **Prefix/suffix support** — Prepend/append to all generated tokens
- ✅ **Field-based generation** — 20+ fields across multiple categories
- ✅ **Streaming architecture** — Memory-efficient token generation

### 🔄 Transforms (17+ available)
- ✅ **Case transforms** — uppercase, lowercase, capitalize, toggle_case, title_case
- ✅ **Leet speak** — basic, full, random leet variations
- ✅ **Homoglyphs** — single, random, full expansion
- ✅ **Keyboard shifts** — adjacent key substitutions
- ✅ **Emoji injection** — insertion and random placement
- ✅ **Append numbers** — suffix with configurable digit patterns
- ✅ **String reversal** — reverse entire tokens
- ✅ **Pluralization** — English pluralization rules
- ✅ **Diacritics** — strip unicode marks

### 🎛️ Filters & Quality
- ✅ **Length validation** — Min/max character constraints
- ✅ **Charset filtering** — Allowlist/blocklist character validation
- ✅ **Entropy calculation** — Shannon entropy scoring
- ✅ **Quality scoring** — 0.0-1.0 quality rating system
- ✅ **Pronounceability** — Basic pronunciation quality checks

### 💾 Output & Storage
- ✅ **Text output** — Plain UTF-8 TXT format
- ✅ **Compression formats** — GZIP, BZIP2, LZ4, ZSTD
- ✅ **JSON output** — JSONL (one JSON per line)
- ✅ **CSV export** — Comma-separated values with headers

### 📋 Presets (5 Built-in)
1. **pentest_default** — Standard pentesting wordlist
2. **meme_humor_pack** — Creative wordlist with humor
3. **api_dev_wordlist** — API endpoint patterns
4. **social_media_usernames** — Social media handles
5. **pattern_basic** — Crunch-style pattern examples

---

## Usage Examples

### Example 1: Basic Generation
```bash
# Generate all 3-character combinations from 'abc'
omni run --min 3 --max 3 --charset "abc" -o output.txt

# View first 10 lines
head -10 output.txt
```

### Example 2: With Transformations
```bash
# Generate with leet speak
omni run \
  --min 5 \
  --max 10 \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  --prefix "admin_" \
  --suffix "!2024" \
  --transforms leet_basic \
  --transforms append_numbers_4 \
  -o output.txt \
  --sample-size 1000
```

### Example 3: Using Presets
```bash
# List available presets
omni list-presets

# Preview pentest preset (show 50 samples)
omni preview --preset pentest_default --sample-size 50

# Generate full wordlist
omni run --preset pentest_default -o pentest.txt --sample-size 10000
```

### Example 4: Compressed Output
```bash
# Generate with GZIP compression
omni run \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  --min 6 \
  --max 12 \
  --compress gzip \
  -o wordlist.txt.gz \
  --sample-size 50000

# Generate with ZSTD (faster compression)
omni run \
  --charset "abcdefghijklmnopqrstuvwxyz0123456789" \
  --min 6 \
  --max 12 \
  --compress zstd \
  -o wordlist.txt.zst
```

### Example 5: JSON Output
```bash
# Generate as JSONL (one JSON per line)
omni run \
  --charset "abc123" \
  --min 4 \
  --max 6 \
  --format jsonl \
  -o output.jsonl \
  --sample-size 100

# View the output
cat output.jsonl | head -5
# Each line is: {"token":"abc1","entropy":2.3,"length":4}
```

### Example 6: Field-Based Generation
```bash
# List all field categories
omni fields --categories

# List fields in a specific category
omni fields --category personal

# Search for fields
omni fields --search name
```

---

## CLI Command Reference

### `omni run` — Generate a wordlist
```bash
omni run [OPTIONS]
```

**Key options:**
- `--min <LEN>` — Minimum word length (default: 1)
- `--max <LEN>` — Maximum word length (default: 10)
- `--charset <CHARS>` — Character set to use
- `--prefix <STR>` — Prepend to each token
- `--suffix <STR>` — Append to each token
- `--preset <NAME>` — Use a named preset
- `--compress <FORMAT>` — Compress output (gzip, bzip2, lz4, zstd)
- `--format <FMT>` — Output format (txt, jsonl, csv)
- `-o, --output <FILE>` — Output file path
- `-s, --sample-size <N>` — Limit output to N tokens
- `--transforms <NAME>` — Apply transforms (can be used multiple times)
- `--dedupe` — Enable deduplication

### `omni preview` — Sample generation before full run
```bash
omni preview [OPTIONS]
```

**Options:**
- `--preset <NAME>` — Preview a preset
- `--sample-size <N>` — Number of samples to show (default: 10)
- `--min <LEN>`, `--max <LEN>` — Length constraints

### `omni list-presets` — Show available presets
```bash
omni list-presets
```

### `omni show-preset` — Display preset details
```bash
omni show-preset <PRESET_NAME>
```

### `omni fields` — Browse available fields
```bash
omni fields [OPTIONS]
```

**Options:**
- `--categories` — List all field categories
- `--category <NAME>` — List fields in a category
- `--search <QUERY>` — Search for fields

### `omni info` — Show version and system info
```bash
omni info
```

---

## Project Structure

```
OmniWordlistPro/
├── omniwordlist/           # Python package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── error.py            # Error types
│   ├── charset.py          # Character sets & patterns
│   ├── fields.py           # Field taxonomy
│   ├── generator.py        # Core generation engine
│   ├── transforms.py       # Transform pipeline
│   ├── filters.py          # Quality & validation
│   ├── storage.py          # Output & compression
│   └── presets.py          # Preset management
│
├── tests/                  # Test suite
│   └── test_basic.py       # Basic functionality tests
│
├── setup.py                # Package setup
├── requirements.txt        # Python dependencies
├── README.md               # Original Python README
└── README_PYTHON.md        # This file
```

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest

# Run tests
pytest tests/ -v
```

### Adding New Transforms

1. Edit `omniwordlist/transforms.py`
2. Create a new Transform class
3. Add to `TRANSFORM_REGISTRY`
4. Add tests in `tests/test_basic.py`

### Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch
3. Make your changes and add tests
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

---

## Performance Comparison

| Feature | Python Version | Python Version |
|---------|---------------|--------------|
| Installation | ✅ Easy (pip) | ⚠️ Requires Python toolchain |
| Startup time | Fast | Very Fast |
| Generation speed | Good | Excellent |
| Memory usage | Low | Very Low |
| Cross-platform | ✅ Excellent | ✅ Excellent |
| Extensibility | ✅ Easy (Python) | Harder (Python) |

**When to use Python version:**
- Quick installation needed
- Easy to modify/extend
- Good enough performance
- Python-friendly environment

**When to use Python version:**
- Maximum performance needed
- Very large wordlists (billions of tokens)
- Production deployments
- Minimal memory footprint required

---

## Dependencies

Core dependencies:
- `click` — CLI framework
- `rich` — Terminal output formatting
- `pydantic` — Data validation
- `lz4`, `zstandard` — Compression support

Optional:
- `unidecode` — Diacritic stripping
- `Levenshtein` — String similarity
- `pytest` — Testing

---

## Troubleshooting

### Issue: `omni: command not found`

**Solution:** Make sure the package is installed and your PATH includes Python scripts:

```bash
pip install -e .
# Or add ~/.local/bin to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: Missing compression support

**Solution:** Install optional compression libraries:

```bash
pip install lz4 zstandard
```

### Issue: Tests failing

**Solution:** Make sure all dependencies are installed:

```bash
pip install -e .
pip install pytest
pytest tests/ -v
```

---

## License

MIT License — See LICENSE file for details

---

## Support & Links

- **Repository:** https://github.com/AaryanBansal-dev/OmniWordlistPro
- **Issues:** https://github.com/AaryanBansal-dev/OmniWordlistPro/issues
- **Original Python Version:** See main README.md

---

## Acknowledgments

This Python implementation maintains the architecture and feature set of the original Python version while making the tool more accessible to the Python community.
