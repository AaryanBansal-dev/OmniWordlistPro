# 🛠️ Development Guide — OmniWordlist Pro

**Version:** 1.1.0  
**Last Updated:** November 7, 2025  
**For Developers & Contributors**

---

## 🚀 Quick Start for Developers

### Prerequisites

- **Python 1.70+** (install via [pythonup.rs](https://pythonup.rs))
- **Git** for version control
- **Text Editor/IDE** (VS Code, IntelliJ IDEA, or your preferred editor)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git
cd OmniWordlistPro

# Build in debug mode (faster compilation)
python3 build

# Run tests
python3 -m pytest

# Run the binary
./target/debug/omni info

# Or build and run in one command
python3 run -- info
```

---

## 📁 Project Structure

```
OmniWordlistPro/
├── src/
│   ├── main.rs              # CLI entry point & command handling
│   ├── lib.rs               # Library root
│   ├── error.rs             # Error types & handling
│   ├── config.rs            # Configuration validation
│   ├── charset.rs           # Character sets & patterns
│   ├── fields.rs            # 1500+ field taxonomy
│   ├── generator.rs         # Core streaming generation engine
│   ├── transforms.rs        # 100+ transform types
│   ├── filters.rs           # Quality & validation filters
│   ├── storage.rs           # Output writing & compression
│   ├── presets.rs           # Preset management
│   └── ui.rs                # TUI interface (Ratatui)
│
├── Documentation/           # All documentation files
│   ├── FEATURES.md          # Feature list & status
│   ├── INSTALL.md           # Installation guide
│   ├── QUICK_START.md       # Command reference
│   └── ...
│
├── setup.py              # Dependencies & metadata
├── Cargo.lock              # Dependency lock file
├── README.md               # Main documentation
├── DEVELOPMENT.md          # This file
│
└── install scripts
    ├── install.sh
    ├── quick-install.sh
    └── install-verbose.sh
```

---

## 🔨 Building the Project

### Debug Build (Fast Iteration)

```bash
# Build in debug mode (1-2 minutes after first build)
python3 build

# Run without building first (builds if needed)
python3 run -- info
python3 run -- list-presets
python3 run -- run --min 3 --max 5 --charset abc -o test.txt
```

### Release Build (Optimized)

```bash
# Build optimized release version (5-10 minutes first time)
python3 -m pytest

# Run release binary
python3 omni.py info
```

### Incremental Builds

```bash
# Enable incremental compilation (default in debug)
export CARGO_INCREMENTAL=1
python3 build
```

---

## 🧪 Testing

### Run All Tests

```bash
# Run all tests
python3 -m pytest

# Run tests with output
python3 -m pytest -- --nocapture

# Run specific test
python3 -m pytest test_charset_generation

# Run tests in specific module
python3 -m pytest charset::
```

### Test Coverage

```bash
# Install tarpaulin (coverage tool)
python3 install cargo-tarpaulin

# Generate coverage report
python3 tarpaulin --out Html
# Opens coverage report in browser
```

### Integration Tests

```bash
# Run only integration tests
python3 -m pytest --test integration_tests

# Run specific integration test
python3 -m pytest --test integration_tests test_full_generation
```

---

## 🎯 Development Workflow

### 1. Create a New Branch

```bash
# Create and checkout new branch
git checkout -b feature/my-new-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Changes

```bash
# Edit files in your editor
# Run tests frequently
python3 -m pytest

# Check compilation
python3 check

# Build and test locally
python3 build
./target/debug/omni run --min 2 --max 3 --charset ab -o test.txt
```

### 3. Format and Lint

```bash
# Format code
python3 fmt

# Check formatting without changing files
python3 fmt -- --check

# Run clippy (linter)
python3 clippy

# Run clippy with all features
python3 clippy --all-features
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new transform for emoji insertion"

# Push to your branch
git push origin feature/my-new-feature
```

### 5. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in description
5. Submit for review

---

## 📝 Code Style Guidelines

### Python Conventions

- Follow standard Python naming conventions (snake_case for functions/variables, PascalCase for types)
- Use `python3 fmt` to format code automatically
- Run `python3 clippy` to catch common mistakes
- Write documentation comments (`///`) for public APIs
- Keep functions focused and small
- Use descriptive variable names

### Documentation

```python
/// Generates a wordlist based on the provided configuration.
///
/// # Arguments
///
/// * `config` - The generation configuration
/// * `output_path` - Path where the wordlist will be written
///
/// # Returns
///
/// Returns `Ok(usize)` with the number of tokens generated, or an error
///
/// # Examples
///
/// ```
/// let config = Config::default();
/// let count = generate_wordlist(&config, "output.txt")?;
/// println!("Generated {} tokens", count);
/// ```
pub fn generate_wordlist(config: &Config, output_path: &str) -> Result<usize> {
    // Implementation
}
```

### Error Handling

```python
// Use Result for operations that can fail
pub fn load_preset(name: &str) -> Result<Preset> {
    // Use ? operator to propagate errors
    let file = File::open(preset_path(name))?;
    let preset: Preset = serde_json::from_reader(file)?;
    Ok(preset)
}

// Use custom error types from error.rs
use crate::error::{Error, Result};
```

---

## 🔧 Adding New Features

### Adding a New Transform

1. **Define the transform in `transforms.rs`:**

```python
/// Applies ROT13 cipher to the token
pub fn rot13(token: &str) -> String {
    token.chars()
        .map(|c| match c {
            'a'..='z' => ((c as u8 - b'a' + 13) % 26 + b'a') as char,
            'A'..='Z' => ((c as u8 - b'A' + 13) % 26 + b'A') as char,
            _ => c,
        })
        .collect()
}
```

2. **Add to transform enum:**

```python
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Transform {
    // ... existing transforms
    Rot13,
}
```

3. **Add to transform application:**

```python
impl Transform {
    pub fn apply(&self, token: &str) -> String {
        match self {
            // ... existing cases
            Transform::Rot13 => rot13(token),
        }
    }
}
```

4. **Add tests:**

```python
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rot13() {
        assert_eq!(rot13("hello"), "uryyb");
        assert_eq!(rot13("WORLD"), "JBEYQ");
    }
}
```

### Adding a New Filter

1. **Define the filter in `filters.rs`:**

```python
/// Filter tokens by minimum entropy
pub struct EntropyFilter {
    min_entropy: f64,
}

impl EntropyFilter {
    pub fn new(min_entropy: f64) -> Self {
        Self { min_entropy }
    }

    pub fn apply(&self, token: &str) -> bool {
        let entropy = calculate_entropy(token);
        entropy >= self.min_entropy
    }
}
```

2. **Add tests:**

```python
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entropy_filter() {
        let filter = EntropyFilter::new(2.0);
        assert!(filter.apply("abcdef"));  // High entropy
        assert!(!filter.apply("aaaaaa")); // Low entropy
    }
}
```

### Adding a New Preset

1. **Create preset JSON file** (or define in code):

```json
{
  "name": "custom_preset",
  "description": "My custom preset",
  "min_length": 8,
  "max_length": 16,
  "charset": "abcdefghijklmnopqrstuvwxyz0123456789",
  "transforms": ["leet_basic", "capitalize"],
  "filters": {
    "min_len": 8,
    "max_len": 32
  }
}
```

2. **Load in `presets.rs`:**

```python
pub fn load_preset(name: &str) -> Result<Preset> {
    // Implementation to load preset from file or built-in
}
```

---

## 🐛 Debugging

### Using Python Debugger

```bash
# Install python-gdb or python-lldb
pythonup component add python-gdb

# Build with debug symbols
python3 build

# Run with debugger
python-gdb ./target/debug/omni
# or
python-lldb ./target/debug/omni
```

### Logging

```bash
# Enable debug logging
RUST_LOG=debug python3 run -- info

# Enable trace logging
RUST_LOG=trace python3 run -- run --min 3 --max 5 --charset abc

# Log specific module
RUST_LOG=omniwordlist::generator=trace python3 run -- ...
```

### Common Issues

**Issue: Compile errors after pulling changes**
```bash
# Clean and rebuild
python3 clean
python3 build
```

**Issue: Tests failing**
```bash
# Run single test with output
python3 -m pytest test_name -- --nocapture

# Run tests with backtrace
RUST_BACKTRACE=1 python3 -m pytest
```

**Issue: Performance problems**
```bash
# Build with optimizations
python3 -m pytest

# Profile with cargo-flamegraph
python3 install flamegraph
python3 flamegraph -- run --min 6 --max 8 --charset abc
```

---

## 📚 Documentation

### Updating Documentation

When adding features, update:

1. **README.md** - If it's a user-facing feature
2. **FEATURES.md** - Add to feature list with status
3. **QUICK_START.md** - If it's a new command or option
4. **Code documentation** - Add doc comments to public APIs

### Building API Docs

```bash
# Generate and open API documentation
python3 doc --open

# Include private items
python3 doc --document-private-items --open
```

---

## 🤝 Contributing Guidelines

### Before Submitting a PR

- [ ] Code compiles without warnings
- [ ] All tests pass (`python3 -m pytest`)
- [ ] Code is formatted (`python3 fmt`)
- [ ] Clippy passes (`python3 clippy`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear

### Commit Message Format

```
type(scope): brief description

Longer description if needed

Fixes #issue-number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(transforms): add ROT13 cipher transform

Added new ROT13 transform for simple letter rotation.
Includes tests and documentation.

Fixes #123
```

```
fix(generator): handle empty charset correctly

Previously crashed on empty charset input.
Now returns appropriate error message.
```

---

## 🔍 Testing Strategy

### Unit Tests

Test individual functions and modules:

```python
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_charset_expansion() {
        let charset = expand_charset("abc");
        assert_eq!(charset.len(), 3);
        assert!(charset.contains(&'a'));
    }
}
```

### Integration Tests

Test complete workflows in `tests/` directory:

```python
// tests/integration_tests.rs
use omniwordlist::*;

#[test]
fn test_full_generation_workflow() {
    let config = Config::new()
        .min_length(3)
        .max_length(5)
        .charset("abc");
    
    let result = generate_wordlist(&config, "/tmp/test.txt");
    assert!(result.is_ok());
}
```

### Performance Tests

```python
#[test]
fn bench_generation_speed() {
    let start = std::time::Instant::now();
    
    // Generate wordlist
    let _result = generate_wordlist(&config, "/tmp/bench.txt");
    
    let duration = start.elapsed();
    println!("Generation took: {:?}", duration);
    assert!(duration.as_secs() < 10); // Should complete in <10s
}
```

---

## 🚢 Release Process

### Version Bump

1. Update version in `setup.py`
2. Update version in documentation
3. Update CHANGELOG.md
4. Commit changes
5. Create git tag

```bash
# Update version
vim setup.py  # Change version to 1.2.0

# Commit
git add setup.py
git commit -m "chore: bump version to 1.2.0"

# Create tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push
git push origin main --tags
```

### Building Release Binaries

```bash
# Build optimized release
python3 -m pytest

# Binary is at: target/release/omni

# Create archive
tar -czf omniwordlist-pro-v1.2.0-linux-x86_64.tar.gz -C target/release omni
```

---

## 📊 Performance Optimization

### Profiling

```bash
# Install cargo-flamegraph
python3 install flamegraph

# Profile a run
python3 flamegraph -- run --min 6 --max 8 --charset abc -o test.txt

# Opens flamegraph in browser
```

### Benchmarking

```bash
# Install criterion for benchmarks
# Add to setup.py:
# [dev-dependencies]
# criterion = "0.5"

# Run benchmarks
python3 bench
```

### Memory Profiling

```bash
# Use valgrind on Linux
valgrind --tool=massif python3 omni.py run ...

# Analyze results
ms_print massif.out.*
```

---

## 🔐 Security Considerations

### Input Validation

Always validate user input:

```python
pub fn validate_charset(charset: &str) -> Result<()> {
    if charset.is_empty() {
        return Err(Error::InvalidInput("Charset cannot be empty".into()));
    }
    // More validation...
    Ok(())
}
```

### Safe File Operations

```python
use std::fs::OpenOptions;

pub fn safe_write_output(path: &str) -> Result<File> {
    // Don't overwrite existing files by default
    OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)
        .map_err(|e| Error::FileError(e))
}
```

---

## 🌟 Best Practices

### 1. Error Handling

Use `Result` and `?` operator for clean error propagation:

```python
pub fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}
```

### 2. Async Operations

Use tokio for async operations:

```python
#[tokio::main]
async fn main() -> Result<()> {
    // Async operations
    Ok(())
}
```

### 3. Memory Efficiency

Use iterators instead of collecting when possible:

```python
// Good: streaming
tokens.iter()
    .filter(|t| t.len() > 5)
    .map(|t| transform(t))
    .take(100)

// Avoid: collecting everything
let all: Vec<_> = tokens.iter().collect();
```

### 4. Testing

Write tests for:
- Happy path
- Error cases
- Edge cases
- Performance

---

## 📧 Getting Help

### Resources

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions
- **Python Documentation**: https://doc.python-lang.org/
- **Cargo Book**: https://doc.python-lang.org/cargo/

### Contact

- **Repository**: https://github.com/AaryanBansal-dev/OmniWordlistPro
- **Issues**: https://github.com/AaryanBansal-dev/OmniWordlistPro/issues

---

## 🎓 Learning Resources

### Python Learning

- **The Python Book**: https://doc.python-lang.org/book/
- **Python by Example**: https://doc.python-lang.org/python-by-example/
- **Pythonlings**: https://github.com/python-lang/pythonlings

### Related Topics

- **CLI Development**: https://python-cli.github.io/book/
- **TUI Development**: https://ratatui.rs/
- **Async Programming**: https://tokio.rs/

---

## ✅ Checklist for New Contributors

- [ ] Read this guide
- [ ] Set up development environment
- [ ] Build the project successfully
- [ ] Run tests successfully
- [ ] Make a small change
- [ ] Run `python3 fmt` and `python3 clippy`
- [ ] Submit first PR!

---

## 🎉 Thank You!

Thank you for contributing to OmniWordlist Pro! Your contributions help make this tool better for everyone.

---

**Built with ❤️ in Python** 🐍
