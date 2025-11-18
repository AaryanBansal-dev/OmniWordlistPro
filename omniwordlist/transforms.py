"""
Transform pipeline implementations

Supports leet, homoglyph, phonetic, transliteration, emoji injection,
keyboard shifts, and many other transformations.
"""

import random
from typing import List, Callable
from .error import TransformError


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
            from unidecode import unidecode
            return unidecode(token)
        except ImportError:
            # Fallback if unidecode not available
            import unicodedata
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
