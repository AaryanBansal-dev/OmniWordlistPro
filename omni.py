#!/usr/bin/env python3
"""
OmniWordlist Pro - Enterprise-grade wordlist generation tool
All-in-one single-file Python version

Version: 1.1.0
Author: Aaryan Bansal
License: MIT

A complete Python-based wordlist generator combining Crunch-style 
pattern generation with advanced transforms, filters, and preset management.
"""

import gzip
import bz2
import json
import math
import re
import itertools
import random
import hashlib
import sys
from pathlib import Path
from typing import Iterator, List, Set, Optional, Dict, Callable
from dataclasses import dataclass, field

# Third-party imports (with fallbacks)
try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    CLICK_AVAILABLE = True
except ImportError:
    CLICK_AVAILABLE = False
    print("Warning: click and rich not available. Install with: pip install click rich")

try:
    from unidecode import unidecode as _unidecode
    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False
    import unicodedata
    def _unidecode(text):
        return "".join(c for c in unicodedata.normalize("NFD", text)
                      if unicodedata.category(c) != "Mn")

__version__ = "1.1.0"
__author__ = "Aaryan Bansal"



# =============================================================================
# ERROR
# =============================================================================

class OmniError(Exception):
    """Base exception class for OmniWordlist Pro"""
    pass


class ConfigError(OmniError):
    """Configuration validation error"""
    pass


class GeneratorError(OmniError):
    """Error during wordlist generation"""
    pass


class StorageError(OmniError):
    """Error in storage operations"""
    pass


class TransformError(OmniError):
    """Error applying transforms"""
    pass


class FilterError(OmniError):
    """Error applying filters"""
    pass


class PresetError(OmniError):
    """Error loading or saving presets"""
    pass


# =============================================================================
# CHARSET
# =============================================================================

# Predefined character sets
CHARSET_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
CHARSET_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHARSET_DIGITS = "0123456789"
CHARSET_SYMBOLS = "!@#$%^&*()-_=+[]{}\\|;:'\",.<>?/`~"
CHARSET_HEX_LOWER = "0123456789abcdef"
CHARSET_HEX_UPPER = "0123456789ABCDEF"
CHARSET_ALPHANUMERIC = CHARSET_LOWERCASE + CHARSET_UPPERCASE + CHARSET_DIGITS
CHARSET_ALPHANUMSYM = CHARSET_ALPHANUMERIC + CHARSET_SYMBOLS


def expand_pattern(pattern: str, literal_chars: str = None) -> str:
    """
    Expand Crunch-style pattern placeholders
    
    Pattern syntax:
    - @ = lowercase letter (a-z)
    - , = uppercase letter (A-Z) 
    - % = digit (0-9)
    - ^ = symbol
    
    Args:
        pattern: Pattern string with placeholders
        literal_chars: Characters to treat as literals (don't expand)
        
    Returns:
        Expanded charset string
    """
    if not pattern:
        return CHARSET_LOWERCASE
    
    literal_set = set(literal_chars or "")
    charset = ""
    
    for char in pattern:
        if char in literal_set:
            charset += char
        elif char == '@':
            charset += CHARSET_LOWERCASE
        elif char == ',':
            charset += CHARSET_UPPERCASE
        elif char == '%':
            charset += CHARSET_DIGITS
        elif char == '^':
            charset += CHARSET_SYMBOLS
        else:
            charset += char
    
    # Remove duplicates while preserving order
    seen = set()
    result = ""
    for char in charset:
        if char not in seen:
            seen.add(char)
            result += char
    
    return result


def get_charset(name: str) -> str:
    """
    Get predefined charset by name
    
    Args:
        name: Charset name (lowercase, uppercase, digits, symbols, etc.)
        
    Returns:
        Character set string
    """
    charsets = {
        "lowercase": CHARSET_LOWERCASE,
        "uppercase": CHARSET_UPPERCASE,
        "digits": CHARSET_DIGITS,
        "symbols": CHARSET_SYMBOLS,
        "hex-lower": CHARSET_HEX_LOWER,
        "hex-upper": CHARSET_HEX_UPPER,
        "alphanumeric": CHARSET_ALPHANUMERIC,
        "all": CHARSET_ALPHANUMSYM,
    }
    return charsets.get(name.lower(), CHARSET_LOWERCASE)


def merge_charsets(*charsets: str) -> str:
    """
    Merge multiple charsets, removing duplicates
    
    Args:
        *charsets: Variable number of charset strings
        
    Returns:
        Merged charset string
    """
    combined = "".join(charsets)
    
    # Remove duplicates while preserving order
    seen = set()
    result = ""
    for char in combined:
        if char not in seen:
            seen.add(char)
            result += char
    
    return result


# =============================================================================
# CONFIG
# =============================================================================

from typing import Optional, List, Dict


@dataclass
class FilterConfig:
    """Filter configuration"""
    min_len: int = 1
    max_len: int = 100
    charset_filter: Optional[str] = None
    min_entropy: float = 0.0
    max_entropy: float = 100.0
    allow_duplicates: bool = True


@dataclass
class Config:
    """Main configuration for wordlist generation"""
    
    # Length constraints
    min_length: int = 1
    max_length: int = 10
    
    # Character set and pattern
    charset: Optional[str] = None
    pattern: Optional[str] = None
    
    # Resume and range control
    start_string: Optional[str] = None
    end_string: Optional[str] = None
    
    # Output configuration
    output_file: Optional[Path] = None
    compression: Optional[str] = None
    
    # Limits
    max_bytes: Optional[int] = None
    max_lines: Optional[int] = None
    
    # Duplicate control
    duplicate_limit: Optional[str] = None
    
    # Generation options
    invert: bool = False
    literal_chars: Optional[str] = None
    
    # Splitting options
    split_by_bytes: Optional[int] = None
    split_by_lines: Optional[int] = None
    
    # Status and display
    show_status: bool = False
    permutations_only: bool = False
    
    # Prefix/suffix
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    separator: Optional[str] = None
    
    # Field-based generation
    enabled_fields: List[str] = field(default_factory=list)
    
    # Transforms
    transforms: List[str] = field(default_factory=list)
    
    # Filters
    filters: FilterConfig = field(default_factory=FilterConfig)
    
    # Performance
    workers: int = 1
    
    # Persistence
    checkpoint_dir: Optional[Path] = None
    
    # Deduplication
    dedupe: bool = False
    bloom_fp_rate: float = 0.01
    
    # Streaming
    buffer_size: int = 8192
    
    # Logging
    verbose: bool = False
    colorized: bool = True
    
    # Randomization
    seed: Optional[int] = None
    
    # Sample size for preview
    sample_size: Optional[int] = None
    
    # Format
    format: str = "txt"
    
    def validate(self) -> None:
        """Validate configuration"""
        if self.min_length < 1:
            raise ConfigError("min_length must be at least 1")
        
        if self.max_length < self.min_length:
            raise ConfigError("max_length must be >= min_length")
        
        if self.workers < 1:
            raise ConfigError("workers must be at least 1")
        
        if self.bloom_fp_rate < 0 or self.bloom_fp_rate > 1:
            raise ConfigError("bloom_fp_rate must be between 0 and 1")
        
        if self.compression and self.compression not in ["gzip", "bzip2", "lz4", "zstd"]:
            raise ConfigError(f"Unsupported compression format: {self.compression}")
        
        if self.format not in ["txt", "jsonl", "csv"]:
            raise ConfigError(f"Unsupported output format: {self.format}")
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Config':
        """Create Config from dictionary"""
        # Handle nested FilterConfig
        if 'filters' in data and isinstance(data['filters'], dict):
            data['filters'] = FilterConfig(**data['filters'])
        
        # Convert paths
        if 'output_file' in data and data['output_file']:
            data['output_file'] = Path(data['output_file'])
        if 'checkpoint_dir' in data and data['checkpoint_dir']:
            data['checkpoint_dir'] = Path(data['checkpoint_dir'])
        
        return cls(**data)
    
    @classmethod
    def from_json(cls, path: Path) -> 'Config':
        """Load configuration from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_dict(self) -> Dict:
        """Convert Config to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Path):
                result[key] = str(value)
            elif isinstance(value, FilterConfig):
                result[key] = value.__dict__
            else:
                result[key] = value
        return result
    
    def to_json(self, path: Path) -> None:
        """Save configuration to JSON file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


# =============================================================================
# FIELDS
# =============================================================================

from typing import Dict, List, Optional


# Field definitions with metadata
FIELDS = {
    # Personal fields
    "first_name_male_0": {
        "id": "first_name_male_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["John", "Michael", "David", "James", "Robert"],
        "cardinality": 1000,
    },
    "first_name_female_0": {
        "id": "first_name_female_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["Mary", "Sarah", "Jennifer", "Emily", "Jessica"],
        "cardinality": 1000,
    },
    "last_name_0": {
        "id": "last_name_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["Smith", "Johnson", "Williams", "Brown", "Jones"],
        "cardinality": 5000,
    },
    "birth_year": {
        "id": "birth_year",
        "category": "personal",
        "group": "dates",
        "type": "number",
        "examples": ["1990", "1985", "1995", "2000", "1980"],
        "cardinality": 100,
    },
    "birth_month_name": {
        "id": "birth_month_name",
        "category": "personal",
        "group": "dates",
        "type": "string",
        "examples": ["January", "February", "March", "April", "May"],
        "cardinality": 12,
    },
    
    # Company and work
    "company_name": {
        "id": "company_name",
        "category": "professional",
        "group": "company",
        "type": "string",
        "examples": ["Google", "Microsoft", "Apple", "Amazon", "Facebook"],
        "cardinality": 10000,
    },
    "job_title": {
        "id": "job_title",
        "category": "professional",
        "group": "company",
        "type": "string",
        "examples": ["Engineer", "Manager", "Developer", "Designer", "Analyst"],
        "cardinality": 500,
    },
    
    # Technical fields
    "dev_handles": {
        "id": "dev_handles",
        "category": "technical",
        "group": "programming",
        "type": "string",
        "examples": ["admin", "root", "user", "test", "dev"],
        "cardinality": 100,
    },
    "programming_language": {
        "id": "programming_language",
        "category": "technical",
        "group": "programming",
        "type": "string",
        "examples": ["python", "java", "javascript", "cpp", "rust"],
        "cardinality": 50,
    },
    "database_name": {
        "id": "database_name",
        "category": "technical",
        "group": "database",
        "type": "string",
        "examples": ["users", "products", "orders", "customers", "accounts"],
        "cardinality": 200,
    },
    
    # Common suffixes and patterns
    "common_suffix_0": {
        "id": "common_suffix_0",
        "category": "patterns",
        "group": "suffixes",
        "type": "string",
        "examples": ["123", "2024", "!", "2023", "!!", "@123"],
        "cardinality": 100,
    },
    "common_prefix_0": {
        "id": "common_prefix_0",
        "category": "patterns",
        "group": "prefixes",
        "type": "string",
        "examples": ["admin", "test", "demo", "user", "my"],
        "cardinality": 50,
    },
    
    # Meme and humor fields
    "fav_meme_format": {
        "id": "fav_meme_format",
        "category": "humor",
        "group": "memes",
        "type": "string",
        "examples": ["doge", "pepe", "stonks", "distracted", "drake"],
        "cardinality": 100,
    },
    "favorite_joke": {
        "id": "favorite_joke",
        "category": "humor",
        "group": "jokes",
        "type": "string",
        "examples": ["dad", "knock", "pun", "dark", "oneliners"],
        "cardinality": 500,
    },
    "favorite_pun": {
        "id": "favorite_pun",
        "category": "humor",
        "group": "puns",
        "type": "string",
        "examples": ["punny", "wordplay", "dadjoke", "groaner", "clever"],
        "cardinality": 300,
    },
    "go_to_reaction_emoji": {
        "id": "go_to_reaction_emoji",
        "category": "humor",
        "group": "emojis",
        "type": "string",
        "examples": ["😂", "😊", "🔥", "❤️", "👍"],
        "cardinality": 50,
    },
    
    # Music and entertainment
    "favorite_artist": {
        "id": "favorite_artist",
        "category": "entertainment",
        "group": "music",
        "type": "string",
        "examples": ["Beatles", "Drake", "Taylor", "Eminem", "Adele"],
        "cardinality": 1000,
    },
    "favorite_song": {
        "id": "favorite_song",
        "category": "entertainment",
        "group": "music",
        "type": "string",
        "examples": ["Yesterday", "Imagine", "Bohemian", "Stairway", "Thriller"],
        "cardinality": 5000,
    },
    
    # Locations
    "city_name": {
        "id": "city_name",
        "category": "location",
        "group": "geography",
        "type": "string",
        "examples": ["NewYork", "London", "Tokyo", "Paris", "Berlin"],
        "cardinality": 10000,
    },
    "country_name": {
        "id": "country_name",
        "category": "location",
        "group": "geography",
        "type": "string",
        "examples": ["USA", "UK", "Japan", "France", "Germany"],
        "cardinality": 195,
    },
    
    # Animals and pets
    "pet_name": {
        "id": "pet_name",
        "category": "personal",
        "group": "pets",
        "type": "string",
        "examples": ["Max", "Bella", "Charlie", "Lucy", "Cooper"],
        "cardinality": 500,
    },
    "animal_type": {
        "id": "animal_type",
        "category": "personal",
        "group": "pets",
        "type": "string",
        "examples": ["dog", "cat", "bird", "fish", "hamster"],
        "cardinality": 50,
    },
}


class FieldManager:
    """Manage field taxonomy and lookups"""
    
    @staticmethod
    def get_field(field_id: str) -> Optional[Dict]:
        """
        Get field by ID
        
        Args:
            field_id: Field identifier
            
        Returns:
            Field dictionary or None
        """
        return FIELDS.get(field_id)
    
    @staticmethod
    def list_fields() -> List[str]:
        """List all field IDs"""
        return list(FIELDS.keys())
    
    @staticmethod
    def list_categories() -> List[str]:
        """List all field categories"""
        categories = set()
        for field in FIELDS.values():
            categories.add(field['category'])
        return sorted(categories)
    
    @staticmethod
    def get_fields_by_category(category: str) -> List[Dict]:
        """
        Get all fields in a category
        
        Args:
            category: Category name
            
        Returns:
            List of field dictionaries
        """
        return [
            field for field in FIELDS.values()
            if field['category'] == category
        ]
    
    @staticmethod
    def search_fields(query: str) -> List[Dict]:
        """
        Search fields by name or description
        
        Args:
            query: Search query
            
        Returns:
            List of matching fields
        """
        query_lower = query.lower()
        results = []
        
        for field in FIELDS.values():
            if (query_lower in field['id'].lower() or
                query_lower in field['category'].lower() or
                query_lower in field['group'].lower()):
                results.append(field)
        
        return results


# =============================================================================
# TRANSFORMS
# =============================================================================

from typing import List, Callable


# Leet speak mappings
LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3', '€'],
    'i': ['1', '!', '|'],
    'o': ['0', '()'],
    's': ['5', '$', 'z'],
    't': ['7', '+'],
    'l': ['1', '|'],
    'g': ['9', '&', '6'],
    'z': ['2', '~'],
    'b': ['8', '|3', 'ß'],
    'x': ['*'],
}

# Homoglyph mappings
HOMOGLYPH_MAP = {
    'a': ['а', 'ɑ', 'α', 'ａ'],
    'e': ['е', 'ε', 'ｅ'],
    'o': ['о', 'ο', 'ｏ'],
    'p': ['р', 'ρ', 'ｐ'],
    'c': ['с', 'ϲ', 'ｃ'],
    'x': ['х', 'χ', 'ｘ'],
    'h': ['һ', 'ｈ'],
    'n': ['ո', 'ｎ'],
}

# Keyboard shift mappings (QWERTY adjacent keys)
KEYBOARD_SHIFT_MAP = {
    'a': ['q', 's'],
    'e': ['r', 'w', 'd'],
    'i': ['u', 'o', 'k'],
    'o': ['i', 'p', 'l'],
    's': ['a', 'd', 'w', 'x'],
    't': ['r', 'y', 'f', 'g'],
}

# Common emojis for injection
EMOJIS = ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', 
          '😉', '😊', '😇', '❤️', '💕', '💖', '💗', '💙', '💚', '💛',
          '🔥', '✨', '⭐', '🌟', '💫', '🎉', '🎊', '🎈', '🎁', '🏆']


class Transform:
    """Base transform class"""
    
    @staticmethod
    def apply(token: str) -> str:
        """Apply transformation to token"""
        return token


class UppercaseTransform(Transform):
    """Convert to uppercase"""
    
    @staticmethod
    def apply(token: str) -> str:
        return token.upper()


class LowercaseTransform(Transform):
    """Convert to lowercase"""
    
    @staticmethod
    def apply(token: str) -> str:
        return token.lower()


class CapitalizeTransform(Transform):
    """Capitalize first letter"""
    
    @staticmethod
    def apply(token: str) -> str:
        return token.capitalize()


class TitleCaseTransform(Transform):
    """Convert to title case"""
    
    @staticmethod
    def apply(token: str) -> str:
        return token.title()


class ToggleCaseTransform(Transform):
    """Toggle case of each character"""
    
    @staticmethod
    def apply(token: str) -> str:
        return ''.join(c.lower() if c.isupper() else c.upper() for c in token)


class ReverseTransform(Transform):
    """Reverse the token"""
    
    @staticmethod
    def apply(token: str) -> str:
        return token[::-1]


class LeetBasicTransform(Transform):
    """Apply basic leet speak transformation"""
    
    @staticmethod
    def apply(token: str) -> str:
        result = []
        for char in token.lower():
            if char in LEET_MAP:
                result.append(LEET_MAP[char][0])
            else:
                result.append(char)
        return ''.join(result)


class LeetFullTransform(Transform):
    """Apply full leet speak transformation with random choices"""
    
    @staticmethod
    def apply(token: str) -> str:
        result = []
        for char in token.lower():
            if char in LEET_MAP:
                result.append(random.choice(LEET_MAP[char]))
            else:
                result.append(char)
        return ''.join(result)


class HomoglyphSingleTransform(Transform):
    """Replace first matching character with homoglyph"""
    
    @staticmethod
    def apply(token: str) -> str:
        result = list(token.lower())
        for i, char in enumerate(result):
            if char in HOMOGLYPH_MAP:
                result[i] = HOMOGLYPH_MAP[char][0]
                break
        return ''.join(result)


class HomoglyphRandomTransform(Transform):
    """Replace random characters with homoglyphs"""
    
    @staticmethod
    def apply(token: str) -> str:
        result = list(token.lower())
        for i, char in enumerate(result):
            if char in HOMOGLYPH_MAP and random.random() < 0.3:
                result[i] = random.choice(HOMOGLYPH_MAP[char])
        return ''.join(result)


class KeyboardShiftTransform(Transform):
    """Replace characters with adjacent keyboard keys"""
    
    @staticmethod
    def apply(token: str) -> str:
        result = []
        for char in token.lower():
            if char in KEYBOARD_SHIFT_MAP and random.random() < 0.2:
                result.append(random.choice(KEYBOARD_SHIFT_MAP[char]))
            else:
                result.append(char)
        return ''.join(result)


class AppendNumbers4Transform(Transform):
    """Append 4-digit number"""
    
    @staticmethod
    def apply(token: str) -> str:
        return f"{token}{random.randint(0, 9999):04d}"


class AppendNumbers2Transform(Transform):
    """Append 2-digit number"""
    
    @staticmethod
    def apply(token: str) -> str:
        return f"{token}{random.randint(0, 99):02d}"


class AppendYearTransform(Transform):
    """Append year (1900-2099)"""
    
    @staticmethod
    def apply(token: str) -> str:
        return f"{token}{random.randint(1900, 2099)}"


class EmojiInsertionTransform(Transform):
    """Insert random emoji at random position"""
    
    @staticmethod
    def apply(token: str) -> str:
        if not token:
            return token
        pos = random.randint(0, len(token))
        emoji = random.choice(EMOJIS)
        return token[:pos] + emoji + token[pos:]


class PluralizationTransform(Transform):
    """Simple English pluralization"""
    
    @staticmethod
    def apply(token: str) -> str:
        if not token:
            return token
        
        lower = token.lower()
        
        # Handle irregular plurals
        irregulars = {
            'man': 'men', 'woman': 'women', 'child': 'children',
            'person': 'people', 'foot': 'feet', 'tooth': 'teeth',
            'mouse': 'mice', 'goose': 'geese'
        }
        
        if lower in irregulars:
            return irregulars[lower]
        
        # Regular pluralization rules
        if lower.endswith('s') or lower.endswith('x') or lower.endswith('z') or \
           lower.endswith('ch') or lower.endswith('sh'):
            return token + 'es'
        elif lower.endswith('y') and len(lower) > 1 and lower[-2] not in 'aeiou':
            return token[:-1] + 'ies'
        elif lower.endswith('f'):
            return token[:-1] + 'ves'
        elif lower.endswith('fe'):
            return token[:-2] + 'ves'
        else:
            return token + 's'


class DiacriticsStripTransform(Transform):
    """Strip diacritics from characters"""
    
    @staticmethod
    def apply(token: str) -> str:
        try:
            return unidecode(token)
        except ImportError:
            # Fallback if unidecode not available
            return ''.join(c for c in unicodedata.normalize('NFD', token)
                          if unicodedata.category(c) != 'Mn')


# Transform registry
TRANSFORM_REGISTRY = {
    'uppercase': UppercaseTransform,
    'lowercase': LowercaseTransform,
    'capitalize': CapitalizeTransform,
    'title_case': TitleCaseTransform,
    'toggle_case': ToggleCaseTransform,
    'reverse': ReverseTransform,
    'leet_basic': LeetBasicTransform,
    'leet_full': LeetFullTransform,
    'homoglyph_single': HomoglyphSingleTransform,
    'homoglyph_random': HomoglyphRandomTransform,
    'keyboard_shift': KeyboardShiftTransform,
    'append_numbers_4': AppendNumbers4Transform,
    'append_numbers_2': AppendNumbers2Transform,
    'append_year': AppendYearTransform,
    'emoji_insertion': EmojiInsertionTransform,
    'pluralization': PluralizationTransform,
    'diacritics_strip': DiacriticsStripTransform,
}


def get_transform(name: str) -> Transform:
    """Get transform by name"""
    if name not in TRANSFORM_REGISTRY:
        raise TransformError(f"Unknown transform: {name}")
    return TRANSFORM_REGISTRY[name]


def apply_transforms(token: str, transform_names: List[str]) -> str:
    """Apply a pipeline of transforms to a token"""
    result = token
    for name in transform_names:
        transform = get_transform(name)
        result = transform.apply(result)
    return result


def list_transforms() -> List[str]:
    """List all available transforms"""
    return sorted(TRANSFORM_REGISTRY.keys())


# =============================================================================
# FILTERS
# =============================================================================

from typing import Optional


def calculate_entropy(token: str) -> float:
    """
    Calculate Shannon entropy of a string
    
    Args:
        token: String to calculate entropy for
        
    Returns:
        Shannon entropy value
    """
    if not token:
        return 0.0
    
    # Count character frequencies
    freq = {}
    for char in token:
        freq[char] = freq.get(char, 0) + 1
    
    # Calculate entropy
    length = len(token)
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy


def calculate_quality_score(token: str) -> float:
    """
    Calculate quality score (0.0 to 1.0)
    
    Considers:
    - Length (longer is better up to a point)
    - Character diversity
    - Entropy
    
    Args:
        token: String to score
        
    Returns:
        Quality score between 0.0 and 1.0
    """
    if not token:
        return 0.0
    
    # Length score (optimal around 8-16 characters)
    length = len(token)
    if length < 4:
        length_score = length / 4.0
    elif length <= 16:
        length_score = 1.0
    else:
        length_score = max(0.5, 1.0 - (length - 16) / 32.0)
    
    # Character diversity score
    unique_chars = len(set(token))
    diversity_score = min(1.0, unique_chars / 10.0)
    
    # Entropy score (normalized)
    entropy = calculate_entropy(token)
    max_entropy = math.log2(len(set(token))) if token else 0
    entropy_score = entropy / max_entropy if max_entropy > 0 else 0
    
    # Combined score
    return (length_score * 0.4 + diversity_score * 0.3 + entropy_score * 0.3)


def check_pronounceability(token: str) -> float:
    """
    Basic pronounceability check
    
    Returns a score between 0.0 (unpronounceable) and 1.0 (pronounceable)
    
    Args:
        token: String to check
        
    Returns:
        Pronounceability score
    """
    if not token:
        return 0.0
    
    vowels = set('aeiouAEIOU')
    consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
    
    # Count vowel and consonant sequences
    prev_type = None
    max_sequence = 0
    current_sequence = 0
    
    for char in token:
        if char in vowels:
            current_type = 'vowel'
        elif char in consonants:
            current_type = 'consonant'
        else:
            current_type = None
        
        if current_type == prev_type and current_type is not None:
            current_sequence += 1
            max_sequence = max(max_sequence, current_sequence)
        else:
            current_sequence = 1
        
        prev_type = current_type
    
    # Penalize long sequences of same type
    if max_sequence > 3:
        return max(0.0, 1.0 - (max_sequence - 3) * 0.2)
    
    # Check vowel to consonant ratio
    vowel_count = sum(1 for c in token if c in vowels)
    consonant_count = sum(1 for c in token if c in consonants)
    total = vowel_count + consonant_count
    
    if total == 0:
        return 0.0
    
    vowel_ratio = vowel_count / total
    
    # Optimal ratio is around 0.3-0.5
    if 0.3 <= vowel_ratio <= 0.5:
        return 1.0
    elif vowel_ratio < 0.3:
        return max(0.0, vowel_ratio / 0.3)
    else:
        return max(0.0, 1.0 - (vowel_ratio - 0.5) / 0.5)


class TokenFilter:
    """Base token filter"""
    
    def __init__(self, config: FilterConfig):
        self.config = config
    
    def should_include(self, token: str) -> bool:
        """Check if token should be included"""
        return True


class LengthFilter(TokenFilter):
    """Filter tokens by length"""
    
    def should_include(self, token: str) -> bool:
        length = len(token)
        return self.config.min_len <= length <= self.config.max_len


class CharsetFilter(TokenFilter):
    """Filter tokens by allowed characters"""
    
    def should_include(self, token: str) -> bool:
        if not self.config.charset_filter:
            return True
        
        allowed = set(self.config.charset_filter)
        return all(c in allowed for c in token)


class EntropyFilter(TokenFilter):
    """Filter tokens by entropy"""
    
    def should_include(self, token: str) -> bool:
        entropy = calculate_entropy(token)
        return self.config.min_entropy <= entropy <= self.config.max_entropy


class QualityFilter(TokenFilter):
    """Filter tokens by quality score"""
    
    def __init__(self, config: FilterConfig, min_quality: float = 0.3):
        super().__init__(config)
        self.min_quality = min_quality
    
    def should_include(self, token: str) -> bool:
        quality = calculate_quality_score(token)
        return quality >= self.min_quality


class RegexFilter(TokenFilter):
    """Filter tokens by regex pattern"""
    
    def __init__(self, config: FilterConfig, pattern: str, match: bool = True):
        super().__init__(config)
        self.pattern = re.compile(pattern)
        self.match = match
    
    def should_include(self, token: str) -> bool:
        matches = bool(self.pattern.search(token))
        return matches if self.match else not matches


class CompositeFilter(TokenFilter):
    """Combine multiple filters"""
    
    def __init__(self, config: FilterConfig, filters: list = None):
        super().__init__(config)
        self.filters = filters or []
    
    def add_filter(self, filter_obj: TokenFilter):
        """Add a filter to the composite"""
        self.filters.append(filter_obj)
    
    def should_include(self, token: str) -> bool:
        """Token must pass all filters"""
        return all(f.should_include(token) for f in self.filters)


def create_filter_pipeline(config: FilterConfig) -> CompositeFilter:
    """Create a filter pipeline from configuration"""
    composite = CompositeFilter(config)
    
    # Always add length filter
    composite.add_filter(LengthFilter(config))
    
    # Add charset filter if specified
    if config.charset_filter:
        composite.add_filter(CharsetFilter(config))
    
    # Add entropy filter if specified
    if config.min_entropy > 0 or config.max_entropy < 100:
        composite.add_filter(EntropyFilter(config))
    
    return composite


# =============================================================================
# STORAGE
# =============================================================================

from typing import Iterator, Optional


class OutputWriter:
    """Base output writer"""
    
    def __init__(self, path: Path, compression: Optional[str] = None, format: str = "txt"):
        """
        Initialize output writer
        
        Args:
            path: Output file path
            compression: Compression format (gzip, bzip2, lz4, zstd)
            format: Output format (txt, jsonl, csv)
        """
        self.path = path
        self.compression = compression
        self.format = format
        self.file_handle = None
        self.bytes_written = 0
        self.lines_written = 0
    
    def open(self):
        """Open output file"""
        # Ensure parent directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open with appropriate compression
        if self.compression == "gzip":
            self.file_handle = gzip.open(self.path, 'wt', encoding='utf-8')
        elif self.compression == "bzip2":
            self.file_handle = bz2.open(self.path, 'wt', encoding='utf-8')
        elif self.compression == "lz4":
            try:
                self.file_handle = lz4.frame.open(self.path, 'wt', encoding='utf-8')
            except ImportError:
                raise StorageError("lz4 compression requires lz4 package")
        elif self.compression == "zstd":
            try:
                cctx = zstd.ZstdCompressor()
                self.file_handle = cctx.stream_writer(open(self.path, 'wb'))
            except ImportError:
                raise StorageError("zstd compression requires zstandard package")
        else:
            self.file_handle = open(self.path, 'w', encoding='utf-8')
        
        # Write CSV header if needed
        if self.format == "csv":
            self._write_line("token,entropy,length")
    
    def write(self, token: str, metadata: dict = None):
        """
        Write a token to output
        
        Args:
            token: Token to write
            metadata: Optional metadata
        """
        if not self.file_handle:
            raise StorageError("Output file not opened")
        
        if self.format == "txt":
            line = token + "\n"
        elif self.format == "jsonl":
            data = {
                "token": token,
                "entropy": calculate_entropy(token),
                "length": len(token)
            }
            if metadata:
                data.update(metadata)
            line = json.dumps(data) + "\n"
        elif self.format == "csv":
            entropy = calculate_entropy(token)
            line = f'"{token}",{entropy},{len(token)}\n'
        else:
            line = token + "\n"
        
        self._write_line(line)
    
    def _write_line(self, line: str):
        """Internal method to write line"""
        if self.compression == "zstd":
            # zstd needs bytes
            self.file_handle.write(line.encode('utf-8'))
        else:
            self.file_handle.write(line)
        
        self.bytes_written += len(line.encode('utf-8'))
        self.lines_written += 1
    
    def close(self):
        """Close output file"""
        if self.file_handle:
            if self.compression == "zstd":
                # Flush zstd compressor
                try:
                    self.file_handle.flush()
                except:
                    pass
            self.file_handle.close()
            self.file_handle = None
    
    def __enter__(self):
        """Context manager entry"""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class CheckpointManager:
    """Manage generation checkpoints for resume capability"""
    
    def __init__(self, checkpoint_dir: Path):
        """
        Initialize checkpoint manager
        
        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(self, job_id: str, state: dict):
        """
        Save checkpoint state
        
        Args:
            job_id: Job identifier
            state: State dictionary to save
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_checkpoint(self, job_id: str) -> Optional[dict]:
        """
        Load checkpoint state
        
        Args:
            job_id: Job identifier
            
        Returns:
            State dictionary or None
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        if not checkpoint_path.exists():
            return None
        
        with open(checkpoint_path, 'r') as f:
            return json.load(f)
    
    def delete_checkpoint(self, job_id: str):
        """
        Delete checkpoint
        
        Args:
            job_id: Job identifier
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        if checkpoint_path.exists():
            checkpoint_path.unlink()


def write_tokens_to_file(tokens: Iterator[str], output_path: Path, 
                        compression: Optional[str] = None, 
                        format: str = "txt") -> int:
    """
    Write tokens to file with optional compression
    
    Args:
        tokens: Iterator of tokens
        output_path: Output file path
        compression: Optional compression format
        format: Output format
        
    Returns:
        Number of tokens written
    """
    count = 0
    with OutputWriter(output_path, compression, format) as writer:
        for token in tokens:
            writer.write(token)
            count += 1
    return count


# =============================================================================
# PRESETS
# =============================================================================

from typing import Dict, List, Optional


# Built-in presets
BUILTIN_PRESETS = {
    "pentest_default": {
        "name": "pentest_default",
        "description": "Standard pentesting wordlist",
        "config": {
            "min_length": 6,
            "max_length": 16,
            "charset": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "enabled_fields": ["company_name", "dev_handles", "first_name_male_0", "birth_year"],
            "transforms": ["leet_basic", "append_numbers_4"],
            "filters": {
                "min_len": 6,
                "max_len": 32,
            },
            "dedupe": True,
        }
    },
    "meme_humor_pack": {
        "name": "meme_humor_pack",
        "description": "Creative wordlist with humor",
        "config": {
            "min_length": 3,
            "max_length": 20,
            "enabled_fields": ["fav_meme_format", "favorite_joke", "favorite_pun", "go_to_reaction_emoji"],
            "transforms": ["emoji_insertion", "capitalize"],
            "filters": {
                "min_len": 3,
                "max_len": 50,
            },
        }
    },
    "api_dev_wordlist": {
        "name": "api_dev_wordlist",
        "description": "API endpoint patterns",
        "config": {
            "min_length": 4,
            "max_length": 20,
            "enabled_fields": ["dev_handles", "programming_language", "database_name"],
            "transforms": ["lowercase", "capitalize"],
            "prefix": "/api/",
            "filters": {
                "min_len": 4,
                "max_len": 50,
            },
        }
    },
    "social_media_usernames": {
        "name": "social_media_usernames",
        "description": "Social media handles",
        "config": {
            "min_length": 3,
            "max_length": 15,
            "enabled_fields": ["first_name_male_0", "first_name_female_0", "last_name_0"],
            "transforms": ["lowercase", "append_numbers_2"],
            "filters": {
                "min_len": 3,
                "max_len": 20,
            },
        }
    },
    "pattern_basic": {
        "name": "pattern_basic",
        "description": "Crunch-style pattern examples",
        "config": {
            "min_length": 4,
            "max_length": 8,
            "pattern": "pass%%",  # pass + 2 digits
            "filters": {
                "min_len": 4,
                "max_len": 10,
            },
        }
    },
}


class PresetManager:
    """Manage presets"""
    
    def __init__(self, preset_dir: Optional[Path] = None):
        """
        Initialize preset manager
        
        Args:
            preset_dir: Directory for custom presets
        """
        self.preset_dir = preset_dir or Path.home() / ".omniwordlist" / "presets"
        self.preset_dir.mkdir(parents=True, exist_ok=True)
    
    def list_presets(self) -> List[str]:
        """List all available presets (built-in and custom)"""
        presets = list(BUILTIN_PRESETS.keys())
        
        # Add custom presets
        if self.preset_dir.exists():
            for preset_file in self.preset_dir.glob("*.json"):
                preset_name = preset_file.stem
                if preset_name not in presets:
                    presets.append(preset_name)
        
        return sorted(presets)
    
    def get_preset(self, name: str) -> Dict:
        """
        Get preset by name
        
        Args:
            name: Preset name
            
        Returns:
            Preset dictionary
        """
        # Check built-in presets first
        if name in BUILTIN_PRESETS:
            return BUILTIN_PRESETS[name]
        
        # Check custom presets
        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            with open(preset_path, 'r') as f:
                return json.load(f)
        
        raise PresetError(f"Preset not found: {name}")
    
    def get_preset_config(self, name: str) -> Config:
        """
        Get preset as Config object
        
        Args:
            name: Preset name
            
        Returns:
            Config object
        """
        preset = self.get_preset(name)
        return Config.from_dict(preset['config'])
    
    def save_preset(self, name: str, description: str, config: Config):
        """
        Save a custom preset
        
        Args:
            name: Preset name
            description: Preset description
            config: Configuration to save
        """
        preset_data = {
            "name": name,
            "description": description,
            "config": config.to_dict(),
        }
        
        preset_path = self.preset_dir / f"{name}.json"
        with open(preset_path, 'w') as f:
            json.dump(preset_data, f, indent=2)
    
    def delete_preset(self, name: str):
        """
        Delete a custom preset
        
        Args:
            name: Preset name
        """
        if name in BUILTIN_PRESETS:
            raise PresetError(f"Cannot delete built-in preset: {name}")
        
        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            preset_path.unlink()
        else:
            raise PresetError(f"Preset not found: {name}")
    
    def show_preset(self, name: str) -> str:
        """
        Show preset details as formatted string
        
        Args:
            name: Preset name
            
        Returns:
            Formatted preset information
        """
        preset = self.get_preset(name)
        
        lines = [
            f"Preset: {preset['name']}",
            f"Description: {preset['description']}",
            "",
            "Configuration:",
        ]
        
        config = preset['config']
        for key, value in sorted(config.items()):
            if value:
                lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)


# =============================================================================
# GENERATOR
# =============================================================================

from typing import Iterator, List, Set, Optional


class Generator:
    """Main wordlist generator"""
    
    def __init__(self, config: Config):
        """
        Initialize generator
        
        Args:
            config: Configuration object
        """
        config.validate()
        self.config = config
        self.tokens_generated = 0
        self.dedup_hashes: Set[str] = set()
        
        # Initialize random seed if specified
        if config.seed is not None:
            random.seed(config.seed)
        
        # Create filter pipeline
        self.filter_pipeline = create_filter_pipeline(config.filters)
    
    def generate(self) -> Iterator[str]:
        """
        Generate tokens based on configuration
        
        Yields:
            Generated tokens
        """
        # Determine generation mode
        if self.config.pattern:
            yield from self._generate_pattern()
        elif self.config.enabled_fields:
            yield from self._generate_fields()
        else:
            yield from self._generate_charset()
    
    def _generate_charset(self) -> Iterator[str]:
        """Generate tokens from charset"""
        charset = self._resolve_charset()
        
        for length in range(self.config.min_length, self.config.max_length + 1):
            if self.config.permutations_only:
                # Generate permutations (no repeating characters)
                for combo in itertools.permutations(charset, length):
                    token = ''.join(combo)
                    processed_token = self._process_token(token)
                    if processed_token is not None:
                        yield processed_token
            else:
                # Generate combinations with replacement
                for combo in itertools.product(charset, repeat=length):
                    token = ''.join(combo)
                    processed_token = self._process_token(token)
                    if processed_token is not None:
                        yield processed_token
    
    def _generate_pattern(self) -> Iterator[str]:
        """Generate tokens using pattern matching (Crunch-style)"""
        pattern = self.config.pattern
        if not pattern:
            raise GeneratorError("No pattern specified")
        
        # Expand pattern to charset
        charset = expand_pattern(pattern, self.config.literal_chars)
        
        # Generate combinations based on pattern length
        length = len(pattern)
        for combo in itertools.product(charset, repeat=length):
            token = ''.join(combo)
            processed_token = self._process_token(token)
            if processed_token is not None:
                yield processed_token
    
    def _generate_fields(self) -> Iterator[str]:
        """Generate tokens using field-based approach"""
        
        if not self.config.enabled_fields:
            raise GeneratorError("No fields enabled")
        
        # Get field values
        field_values = []
        for field_id in self.config.enabled_fields:
            field = FieldManager.get_field(field_id)
            if field:
                field_values.append(field['examples'])
            else:
                # Use field_id as fallback
                field_values.append([field_id])
        
        # Generate combinations of field values
        for combo in itertools.product(*field_values):
            # Join with separator if specified, otherwise concatenate
            if self.config.separator:
                token = self.config.separator.join(combo)
            else:
                token = ''.join(combo)
            
            processed_token = self._process_token(token)
            if processed_token is not None:
                yield processed_token
    
    def _resolve_charset(self) -> str:
        """Resolve charset from configuration"""
        if self.config.charset:
            # Check if it's a named charset (specific known names only)
            named_charsets = ['lowercase', 'uppercase', 'digits', 'symbols', 
                            'hex-lower', 'hex-upper', 'alphanumeric', 'all']
            if self.config.charset in named_charsets:
                return get_charset(self.config.charset)
            # Otherwise treat as custom charset
            return self.config.charset
        
        # Default to lowercase
        return CHARSET_LOWERCASE
    
    def _process_token(self, token: str) -> Optional[str]:
        """
        Process and validate token
        
        Args:
            token: Token to process
            
        Returns:
            Processed token or None if should be filtered
        """
        # Apply prefix/suffix
        if self.config.prefix:
            token = self.config.prefix + token
        if self.config.suffix:
            token = token + self.config.suffix
        
        # Apply transforms
        if self.config.transforms:
            token = apply_transforms(token, self.config.transforms)
        
        # Check filters
        if not self.filter_pipeline.should_include(token):
            return None
        
        # Check start/end boundaries
        if self.config.start_string and token < self.config.start_string:
            return None
        if self.config.end_string and token > self.config.end_string:
            return None
        
        # Deduplication
        if self.config.dedupe:
            token_hash = hashlib.blake2b(token.encode()).hexdigest()
            if token_hash in self.dedup_hashes:
                return None
            self.dedup_hashes.add(token_hash)
        
        # Check limits
        if self.config.max_lines and self.tokens_generated >= self.config.max_lines:
            return None
        
        self.tokens_generated += 1
        return token
    
    def generate_list(self, limit: Optional[int] = None) -> List[str]:
        """
        Generate tokens as a list
        
        Args:
            limit: Optional limit on number of tokens
            
        Returns:
            List of generated tokens
        """
        tokens = []
        for i, token in enumerate(self.generate()):
            tokens.append(token)
            if limit and i + 1 >= limit:
                break
        return tokens
    
    def preview(self, sample_size: int = 10) -> List[str]:
        """
        Generate a preview of tokens
        
        Args:
            sample_size: Number of tokens to preview
            
        Returns:
            List of sample tokens
        """
        return self.generate_list(limit=sample_size)
    
    def estimate_count(self) -> int:
        """
        Estimate total number of tokens to be generated
        
        Returns:
            Estimated token count
        """
        if self.config.max_lines:
            return self.config.max_lines
        
        charset = self._resolve_charset()
        charset_size = len(set(charset))
        
        if self.config.permutations_only:
            # Permutations: P(n, r) = n! / (n-r)!
            total = 0
            for length in range(self.config.min_length, self.config.max_length + 1):
                if length <= charset_size:
                    # Calculate permutation count
                    perm = 1
                    for i in range(length):
                        perm *= (charset_size - i)
                    total += perm
            return total
        else:
            # Combinations with replacement: n^r
            total = 0
            for length in range(self.config.min_length, self.config.max_length + 1):
                total += charset_size ** length
            return total
    
    def get_stats(self) -> dict:
        """
        Get generation statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            'tokens_generated': self.tokens_generated,
            'estimated_total': self.estimate_count(),
            'dedup_cache_size': len(self.dedup_hashes),
            'config': self.config.to_dict(),
        }


# =============================================================================
# CLI
# =============================================================================

console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, verbose):
    """OmniWordlist Pro - Enterprise-grade wordlist generation"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option('--min', 'min_length', type=int, help='Minimum length')
@click.option('--max', 'max_length', type=int, help='Maximum length')
@click.option('--charset', help='Character set')
@click.option('--pattern', help='Pattern (Crunch-style)')
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.option('--compress', type=click.Choice(['gzip', 'bzip2', 'lz4', 'zstd']), help='Compression format')
@click.option('--prefix', help='Prefix for each token')
@click.option('--suffix', help='Suffix for each token')
@click.option('--format', type=click.Choice(['txt', 'jsonl', 'csv']), default='txt', help='Output format')
@click.option('--preset', help='Use a preset')
@click.option('--sample-size', '-s', type=int, help='Limit output to N tokens')
@click.option('--dedupe', is_flag=True, help='Enable deduplication')
@click.option('--transforms', multiple=True, help='Apply transforms')
@click.pass_context
def run(ctx, min_length, max_length, charset, pattern, output, compress, 
        prefix, suffix, format, preset, sample_size, dedupe, transforms):
    """Generate a wordlist"""
    
    verbose = ctx.obj.get('verbose', False)
    
    # Load preset if specified
    if preset:
        preset_mgr = PresetManager()
        config = preset_mgr.get_preset_config(preset)
        if verbose:
            console.print(f"[green]Loaded preset: {preset}[/green]")
    else:
        config = Config()
    
    # Override with command-line options
    if min_length is not None:
        config.min_length = min_length
    if max_length is not None:
        config.max_length = max_length
    if charset:
        config.charset = charset
    if pattern:
        config.pattern = pattern
    if prefix:
        config.prefix = prefix
    if suffix:
        config.suffix = suffix
    if compress:
        config.compression = compress
    if format:
        config.format = format
    if sample_size:
        config.sample_size = sample_size
        config.max_lines = sample_size
    if dedupe:
        config.dedupe = dedupe
    if transforms:
        config.transforms = list(transforms)
    
    config.verbose = verbose
    
    # Validate configuration
    try:
        config.validate()
    except Exception as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        sys.exit(1)
    
    # Create generator
    try:
        generator = Generator(config)
    except Exception as e:
        console.print(f"[red]Generator error: {e}[/red]")
        sys.exit(1)
    
    # Show stats
    if verbose:
        estimated = generator.estimate_count()
        console.print(f"[cyan]Estimated tokens: {estimated:,}[/cyan]")
    
    # Generate and write
    if output:
        output_path = Path(output)
        console.print(f"[green]Generating wordlist to {output_path}...[/green]")
        
        try:
            with OutputWriter(output_path, config.compression, config.format) as writer:
                for token in track(generator.generate(), 
                                 description="Generating...",
                                 total=config.max_lines):
                    writer.write(token)
            
            console.print(f"[green]✓ Generated {generator.tokens_generated:,} tokens[/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]")
        except Exception as e:
            console.print(f"[red]Error writing output: {e}[/red]")
            sys.exit(1)
    else:
        # Write to stdout
        for token in generator.generate():
            print(token)


@cli.command()
@click.option('--preset', help='Preview a preset')
@click.option('--sample-size', type=int, default=10, help='Number of samples')
@click.option('--min', 'min_length', type=int, help='Minimum length')
@click.option('--max', 'max_length', type=int, help='Maximum length')
@click.option('--charset', help='Character set')
@click.pass_context
def preview(ctx, preset, sample_size, min_length, max_length, charset):
    """Preview wordlist generation"""
    
    verbose = ctx.obj.get('verbose', False)
    
    # Load preset if specified
    if preset:
        preset_mgr = PresetManager()
        config = preset_mgr.get_preset_config(preset)
        console.print(f"[green]Previewing preset: {preset}[/green]\n")
    else:
        config = Config()
    
    # Override with command-line options
    if min_length is not None:
        config.min_length = min_length
    if max_length is not None:
        config.max_length = max_length
    if charset:
        config.charset = charset
    
    config.verbose = verbose
    config.sample_size = sample_size
    config.max_lines = sample_size
    
    try:
        generator = Generator(config)
        samples = generator.preview(sample_size)
        
        console.print(f"[cyan]Sample output ({len(samples)} tokens):[/cyan]\n")
        for i, token in enumerate(samples, 1):
            console.print(f"  {i:3d}. {token}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-presets')
def list_presets():
    """List available presets"""
    preset_mgr = PresetManager()
    presets = preset_mgr.list_presets()
    
    console.print("[cyan]Available Presets:[/cyan]\n")
    
    for i, preset_name in enumerate(presets, 1):
        preset = preset_mgr.get_preset(preset_name)
        desc = preset.get('description', 'No description')
        console.print(f"  {i}. [green]{preset_name:25s}[/green] - {desc}")


@cli.command('show-preset')
@click.argument('preset_name')
def show_preset(preset_name):
    """Show preset details"""
    preset_mgr = PresetManager()
    
    try:
        info = preset_mgr.show_preset(preset_name)
        console.print(info)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--categories', is_flag=True, help='List field categories')
@click.option('--category', help='List fields in a category')
@click.option('--search', help='Search for fields')
def fields(categories, category, search):
    """Browse available fields"""
    
    if categories:
        # List categories
        cats = FieldManager.list_categories()
        console.print("[cyan]Field Categories:[/cyan]\n")
        for cat in cats:
            console.print(f"  - {cat}")
    elif category:
        # List fields in category
        field_list = FieldManager.get_fields_by_category(category)
        console.print(f"[cyan]Fields in category '{category}':[/cyan]\n")
        for field in field_list:
            console.print(f"  - {field['id']:30s} ({field['group']})")
    elif search:
        # Search fields
        results = FieldManager.search_fields(search)
        console.print(f"[cyan]Search results for '{search}':[/cyan]\n")
        for field in results:
            console.print(f"  - {field['id']:30s} [{field['category']}/{field['group']}]")
    else:
        # List all fields
        field_list = FieldManager.list_fields()
        console.print(f"[cyan]All Fields ({len(field_list)} total):[/cyan]\n")
        for field_id in field_list[:20]:  # Show first 20
            console.print(f"  - {field_id}")
        if len(field_list) > 20:
            console.print(f"\n  ... and {len(field_list) - 20} more")


@cli.command()
def info():
    """Show version and system info"""
    console.print(f"[cyan]OmniWordlist Pro v{__version__}[/cyan]\n")
    console.print(f"[green]Python-based Enterprise Wordlist Generator[/green]\n")
    
    console.print("[cyan]Supported transforms:[/cyan]")
    transforms = list_transforms()
    for i in range(0, len(transforms), 3):
        row = transforms[i:i+3]
        console.print(f"  {', '.join(row)}")
    
    console.print("\n[cyan]Supported compression:[/cyan]")
    console.print("  gzip, bzip2, lz4, zstd")
    
    console.print("\n[cyan]Supported formats:[/cyan]")
    console.print("  txt, jsonl, csv")


@cli.command()
def tui():
    """Launch interactive TUI (Terminal User Interface)"""
    console.print("[yellow]TUI not yet implemented in Python version[/yellow]")
    console.print("Use the CLI commands for now.")


def main():
    """Main entry point"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()


if __name__ == "__main__":
    if not CLICK_AVAILABLE:
        print("Error: This script requires click and rich packages.")
        print("Please install them: pip install click rich")
        sys.exit(1)
    main()
