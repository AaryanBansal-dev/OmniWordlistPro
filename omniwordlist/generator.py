"""
Core generation engine

Streaming combinator pipeline with checkpoint support and deduplication
"""

import itertools
import random
from typing import Iterator, List, Set, Optional
from pathlib import Path
import hashlib
from .config import Config
from .charset import expand_pattern, get_charset, CHARSET_LOWERCASE
from .transforms import apply_transforms
from .filters import create_filter_pipeline
from .error import GeneratorError


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
        from .fields import FieldManager
        
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
