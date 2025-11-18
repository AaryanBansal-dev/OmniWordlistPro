"""
OmniWordlist Pro - Enterprise-grade wordlist generation library

This package provides a complete wordlist generation framework combining
Crunch-like pattern generation with CUPP-style personalization and
1500+ toggleable fields with advanced transforms.
"""

__version__ = "1.1.0"
__author__ = "Aaryan Bansal"

from .config import Config, FilterConfig
from .generator import Generator
from .error import OmniError

__all__ = [
    'Config',
    'FilterConfig', 
    'Generator',
    'OmniError',
]
