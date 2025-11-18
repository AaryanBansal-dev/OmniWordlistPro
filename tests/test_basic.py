"""
Basic tests for OmniWordlist Pro
"""

import pytest
from pathlib import Path
import tempfile

from omniwordlist import Config, Generator
from omniwordlist.charset import expand_pattern, get_charset, merge_charsets
from omniwordlist.transforms import apply_transforms
from omniwordlist.filters import calculate_entropy, calculate_quality_score
from omniwordlist.fields import FieldManager
from omniwordlist.presets import PresetManager


def test_charset_expand_pattern():
    """Test pattern expansion"""
    # Test lowercase
    assert 'a' in expand_pattern('@')
    assert 'z' in expand_pattern('@')
    
    # Test digits
    assert '0' in expand_pattern('%')
    assert '9' in expand_pattern('%')
    
    # Test mixed
    pattern_result = expand_pattern('@%')
    assert 'a' in pattern_result
    assert '0' in pattern_result


def test_charset_get_charset():
    """Test named charset retrieval"""
    lowercase = get_charset('lowercase')
    assert 'a' in lowercase
    assert 'z' in lowercase
    assert 'A' not in lowercase
    
    digits = get_charset('digits')
    assert '0' in digits
    assert '9' in digits


def test_merge_charsets():
    """Test charset merging"""
    result = merge_charsets('abc', 'def', 'abc')
    assert len(result) == 6  # No duplicates
    assert 'a' in result
    assert 'f' in result


def test_config_validation():
    """Test configuration validation"""
    config = Config(min_length=1, max_length=5)
    config.validate()  # Should not raise
    
    # Invalid config
    config_bad = Config(min_length=10, max_length=5)
    with pytest.raises(Exception):
        config_bad.validate()


def test_generator_basic():
    """Test basic generation"""
    config = Config(
        min_length=2,
        max_length=2,
        charset='ab',
        max_lines=10
    )
    
    generator = Generator(config)
    tokens = generator.generate_list(limit=10)
    
    assert len(tokens) > 0
    assert len(tokens) <= 10
    assert all(len(t) == 2 for t in tokens)
    assert all(c in 'ab' for t in tokens for c in t)


def test_generator_with_transforms():
    """Test generation with transforms"""
    config = Config(
        min_length=3,
        max_length=3,
        charset='abc',
        transforms=['uppercase'],
        max_lines=5
    )
    
    generator = Generator(config)
    tokens = generator.generate_list(limit=5)
    
    assert len(tokens) > 0
    assert all(t.isupper() for t in tokens)


def test_transforms():
    """Test transform functions"""
    # Uppercase
    assert apply_transforms('hello', ['uppercase']) == 'HELLO'
    
    # Lowercase
    assert apply_transforms('HELLO', ['lowercase']) == 'hello'
    
    # Capitalize
    assert apply_transforms('hello', ['capitalize']) == 'Hello'
    
    # Reverse
    assert apply_transforms('hello', ['reverse']) == 'olleh'


def test_filters():
    """Test filter functions"""
    # Entropy
    entropy = calculate_entropy('abcdef')
    assert entropy > 0
    
    # Quality score
    quality = calculate_quality_score('password123')
    assert 0 <= quality <= 1


def test_field_manager():
    """Test field manager"""
    # List fields
    fields = FieldManager.list_fields()
    assert len(fields) > 0
    
    # Get field
    field = FieldManager.get_field('first_name_male_0')
    assert field is not None
    assert 'examples' in field
    
    # List categories
    categories = FieldManager.list_categories()
    assert len(categories) > 0
    assert 'personal' in categories


def test_preset_manager():
    """Test preset manager"""
    preset_mgr = PresetManager()
    
    # List presets
    presets = preset_mgr.list_presets()
    assert len(presets) > 0
    assert 'pentest_default' in presets
    
    # Get preset
    preset = preset_mgr.get_preset('pentest_default')
    assert preset is not None
    assert 'config' in preset
    
    # Get preset config
    config = preset_mgr.get_preset_config('pentest_default')
    assert isinstance(config, Config)


def test_generator_preview():
    """Test preview functionality"""
    config = Config(
        min_length=3,
        max_length=5,
        charset='abc',
    )
    
    generator = Generator(config)
    preview = generator.preview(sample_size=5)
    
    assert len(preview) == 5
    assert all(3 <= len(t) <= 5 for t in preview)


def test_generator_estimate():
    """Test token count estimation"""
    config = Config(
        min_length=2,
        max_length=3,
        charset='ab',
    )
    
    generator = Generator(config)
    estimate = generator.estimate_count()
    
    # For charset 'ab' with lengths 2-3:
    # Length 2: 2^2 = 4 (aa, ab, ba, bb)
    # Length 3: 2^3 = 8
    # Total: 12
    assert estimate == 12


def test_output_writer():
    """Test output writing"""
    from omniwordlist.storage import OutputWriter
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / 'test.txt'
        
        with OutputWriter(output_path) as writer:
            writer.write('test1')
            writer.write('test2')
            writer.write('test3')
        
        # Verify file exists
        assert output_path.exists()
        
        # Verify content
        content = output_path.read_text()
        assert 'test1' in content
        assert 'test2' in content
        assert 'test3' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
