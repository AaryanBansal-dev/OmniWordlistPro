"""
Character set definitions and utilities

Implements Crunch-style character patterns and predefined charsets
"""

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
