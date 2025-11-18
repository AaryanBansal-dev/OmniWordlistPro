"""Configuration validation and management"""

from typing import Optional, List, Dict
from dataclasses import dataclass, field
from pathlib import Path
import json
from .error import ConfigError


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
