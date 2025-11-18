"""
Filtering and quality control

Implements entropy, language detection, regex validation,
and other quality filters.
"""

import math
import re
from typing import Optional
from .error import FilterError
from .config import FilterConfig


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
