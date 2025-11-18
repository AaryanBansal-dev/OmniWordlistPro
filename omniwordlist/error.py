"""Error types and handling for OmniWordlist Pro"""


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
