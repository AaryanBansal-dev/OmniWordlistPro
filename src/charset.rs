/// Character set definitions and utilities
/// 
/// Implements Crunch-style character patterns and predefined charsets

use lazy_static::lazy_static;
use std::collections::HashMap;

lazy_static! {
    pub static ref CHARSETS: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        m.insert("lower", "abcdefghijklmnopqrstuvwxyz");
        m.insert("upper", "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
        m.insert("digit", "0123456789");
        m.insert("symbol", "!@#$%^&*()_+-=[]{}|;:,.<>?");
        m.insert("alpha", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
        m.insert("alnum", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
        m.insert("space", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ");
        m.insert("hex", "0123456789abcdef");
        m.insert("hex_upper", "0123456789ABCDEF");
        m.insert("printable", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>? ");
        m
    };

    pub static ref PATTERN_MARKERS: HashMap<char, &'static str> = {
        let mut m = HashMap::new();
        m.insert('@', "lower");      // lowercase letter
        m.insert('%', "digit");      // digit
        m.insert('^', "symbol");     // symbol
        m.insert(',', "upper");      // uppercase letter
        m.insert('?', "alnum");      // alphanumeric
        m.insert('!', "printable");  // any printable
        m
    };

    pub static ref EMOJI_SETS: HashMap<&'static str, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert("emoji_single", vec![
            "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃",
            "😉", "😊", "😇", "🥰", "😍", "🤩", "😘", "😗", "😚", "😙",
            "🥲", "😋", "😛", "😜", "🤪", "😌", "😔", "😑", "😐", "😶",
            "🤐", "🥵", "🥶", "🥱", "😏", "😓", "😞", "😖", "😢", "😭",
            "😱", "😖", "😣", "😞", "😓", "😩", "😫", "🥺", "😤", "😡",
            "😠", "🤬", "😈", "👿", "💀", "☠️", "💩", "🤡", "👹", "👺",
            "👻", "👽", "👾", "🤖", "😺", "😸", "😹", "😻", "😼", "😽",
        ]);
        m.insert("reaction_emoji", vec![
            "👍", "👎", "👊", "✊", "🤛", "🤜", "✋", "🖐️", "🖖",
            "👌", "🤌", "🤏", "✌️", "🤞", "🫰", "🤟", "🤘", "🤙",
            "🥰", "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍",
            "🤎", "💔", "💕", "💞", "💓", "💗", "💖", "💘", "💝",
            "💟", "💌", "💜", "🔥", "⭐", "✨", "💫", "🌟",
        ]);
        m
    };

    pub static ref MEME_FORMATS: Vec<&'static str> = vec![
        "drake", "loss", "expanding_brain", "surprised_pikachu",
        "laughing_tom_cruise", "doge", "distracted_boyfriend",
        "two_button", "tic_tac_toe", "guy_pointing", "handshake",
        "spider_man_pointing", "success_kid", "bad_luck_brian",
        "grumpy_cat", "confused_cat", "evil_toddler", "arthur_fist",
    ];

    pub static ref MEME_JOKES: Vec<&'static str> = vec![
        "why_did_chicken_cross_road", "knock_knock", "yo_mama",
        "what_do_you_call", "how_many_does_it_take", "dad_joke",
        "light_bulb", "programmer", "genie", "pirate", "skeleton",
    ];

    pub static ref KEYBOARD_PATTERNS: Vec<&'static str> = vec![
        "qwerty", "asdfgh", "zxcvbn", "qazwsx", "qweasd",
        "1qaz2wsx", "123456", "111111", "123123", "password",
    ];

    pub static ref COMMON_LEET_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["4", "@"]);
        m.insert('e', vec!["3", "€"]);
        m.insert('i', vec!["1", "!"]);
        m.insert('o', vec!["0", "()"]);
        m.insert('s', vec!["5", "$"]);
        m.insert('t', vec!["7", "+"]);
        m.insert('l', vec!["1", "|"]);
        m.insert('g', vec!["9", "&"]);
        m.insert('z', vec!["2", "~"]);
        m.insert('b', vec!["8", "|3"]);
        m
    };

    pub static ref HOMOGLYPH_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["а", "ɑ", "α"]);  // Cyrillic, IPA, Greek
        m.insert('e', vec!["е", "ε"]);
        m.insert('o', vec!["о", "ο", "0"]);
        m.insert('p', vec!["р", "ρ"]);
        m.insert('c', vec!["с", "ϲ"]);
        m.insert('x', vec!["х", "χ"]);
        m
    };
}

pub struct CharsetBuilder {
    chars: Vec<char>,
}

impl CharsetBuilder {
    pub fn new() -> Self {
        Self {
            chars: Vec::new(),
        }
    }

    pub fn add_charset(mut self, name: &str) -> crate::Result<Self> {
        if let Some(charset) = CHARSETS.get(name) {
            self.chars.extend(charset.chars());
        } else {
            return Err(crate::Error::InvalidCharset(format!(
                "Unknown charset: {}",
                name
            )));
        }
        Ok(self)
    }

    pub fn add_custom(mut self, charset: &str) -> Self {
        self.chars.extend(charset.chars());
        self
    }

    pub fn build(self) -> String {
        // Remove duplicates while preserving order
        let mut seen = std::collections::HashSet::new();
        self.chars
            .into_iter()
            .filter(|c| seen.insert(*c))
            .collect()
    }

    pub fn build_deduplicated(self) -> String {
        let mut set = std::collections::HashSet::new();
        set.extend(self.chars);
        let mut chars: Vec<_> = set.into_iter().collect();
        chars.sort();
        chars.into_iter().collect()
    }
}

/// Expand pattern into charset using markers
pub fn expand_pattern(pattern: &str, literal_markers: Option<&str>) -> crate::Result<String> {
    let mut charset = String::new();
    let literal_set: std::collections::HashSet<char> = literal_markers
        .unwrap_or("")
        .chars()
        .collect();

    for ch in pattern.chars() {
        if literal_set.contains(&ch) {
            charset.push(ch);
        } else if let Some(name) = PATTERN_MARKERS.get(&ch) {
            if let Some(chars) = CHARSETS.get(name) {
                charset.push_str(chars);
            }
        } else {
            charset.push(ch);
        }
    }

    Ok(charset)
}

/// Load charset from file
pub fn load_charset_file(path: &std::path::Path) -> crate::Result<String> {
    let content = std::fs::read_to_string(path)?;
    Ok(content.trim().to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_charset_builder() {
        let charset = CharsetBuilder::new()
            .add_charset("lower")
            .unwrap()
            .add_charset("digit")
            .unwrap()
            .build();

        assert!(charset.contains('a'));
        assert!(charset.contains('0'));
    }

    #[test]
    fn test_pattern_expansion() {
        let expanded = expand_pattern("@@", None).unwrap();
        assert!(expanded.len() >= 52); // at least lowercase + uppercase
    }
}
