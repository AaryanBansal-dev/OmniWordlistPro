/// Transform pipeline implementations
/// 
/// Supports leet, homoglyph, phonetic, transliteration, emoji injection,
/// keyboard shifts, and many other transformations.

use std::collections::HashMap;
use regex::Regex;
use lazy_static::lazy_static;

lazy_static! {
    static ref LEET_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["4", "@"]);
        m.insert('e', vec!["3", "€"]);
        m.insert('i', vec!["1", "!", "|"]);
        m.insert('o', vec!["0", "()"]);
        m.insert('s', vec!["5", "$", "z"]);
        m.insert('t', vec!["7", "+"]);
        m.insert('l', vec!["1", "|"]);
        m.insert('g', vec!["9", "&", "6"]);
        m.insert('z', vec!["2", "~"]);
        m.insert('b', vec!["8", "|3", "ß"]);
        m.insert('x', vec!["*"]);
        m
    };

    static ref HOMOGLYPH_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["а", "ɑ", "α", "ａ"]);
        m.insert('e', vec!["е", "ε", "ｅ"]);
        m.insert('o', vec!["о", "ο", "ο", "ｏ"]);
        m.insert('p', vec!["р", "ρ", "ｐ"]);
        m.insert('c', vec!["с", "ϲ", "ｃ"]);
        m.insert('x', vec!["х", "χ", "ｘ"]);
        m.insert('h', vec!["һ", "ｈ"]);
        m.insert('n', vec!["ո", "ｎ"]);
        m
    };

    static ref KEYBOARD_SHIFT_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["q", "s"]);
        m.insert('e', vec!["r", "w", "d"]);
        m.insert('i', vec!["u", "o", "k"]);
        m.insert('o', vec!["i", "p", "l"]);
        m.insert('s', vec!["a", "d", "w", "x"]);
        m.insert('t', vec!["r", "y", "f", "g"]);
        m
    };

    static ref DIACRITIC_MAP: HashMap<char, Vec<&'static str>> = {
        let mut m = HashMap::new();
        m.insert('a', vec!["á", "à", "ä", "â", "ã", "å", "ą", "ă"]);
        m.insert('e', vec!["é", "è", "ë", "ê", "ę", "ė"]);
        m.insert('i', vec!["í", "ì", "ï", "î", "į", "ı"]);
        m.insert('o', vec!["ó", "ò", "ö", "ô", "õ", "ø", "ǫ", "ơ"]);
        m.insert('u', vec!["ú", "ù", "ü", "û", "ũ", "ū", "ų", "ư"]);
        m.insert('n', vec!["ñ", "ń", "ň", "ņ"]);
        m.insert('c', vec!["ć", "č", "ç", "ĉ"]);
        m
    };
}

#[derive(Debug, Clone)]
pub enum Transform {
    LeetBasic,
    LeetFull,
    LeetRandom,
    Reverse,
    ToggleCase,
    UpperCase,
    LowerCase,
    TitleCase,
    Capitalize,
    AppendNumbers(usize),
    PrependNumbers(usize),
    AppendSymbols(usize),
    PrependSymbols(usize),
    Homoglyph,
    HomoglyphRandom,
    HomoglyphFull,
    KeyboardShift,
    PhoneticSubstitution,
    TransliterationLatin,
    DiacriticExpand,
    DiacriticStrip,
    EmojiInsertion,
    EmojiRandom,
    PluralizeEnd,
    SingularizeEnd,
    DoubleLast,
    TripleLast,
    ReverseWords,
    InterleaveSpaces,
    RandomInsertSpaces,
    Custom(String),
}

pub struct TransformPipeline {
    transforms: Vec<Transform>,
}

impl TransformPipeline {
    pub fn new() -> Self {
        Self {
            transforms: Vec::new(),
        }
    }

    pub fn add(mut self, transform: Transform) -> Self {
        self.transforms.push(transform);
        self
    }

    pub fn apply(&self, token: &str) -> crate::Result<String> {
        let mut result = token.to_string();
        
        for transform in &self.transforms {
            result = apply_transform(&result, transform)?;
        }
        
        Ok(result)
    }

    pub fn apply_all(&self, tokens: Vec<String>) -> crate::Result<Vec<String>> {
        tokens.into_iter()
            .map(|t| self.apply(&t))
            .collect()
    }
}

fn apply_transform(token: &str, transform: &Transform) -> crate::Result<String> {
    match transform {
        Transform::LeetBasic => apply_leet_basic(token),
        Transform::LeetFull => apply_leet_full(token),
        Transform::LeetRandom => apply_leet_random(token),
        Transform::Reverse => Ok(token.chars().rev().collect()),
        Transform::ToggleCase => Ok(toggle_case(token)),
        Transform::UpperCase => Ok(token.to_uppercase()),
        Transform::LowerCase => Ok(token.to_lowercase()),
        Transform::TitleCase => Ok(to_title_case(token)),
        Transform::Capitalize => Ok(capitalize(token)),
        Transform::AppendNumbers(n) => Ok(format!("{}{}", token, random_digits(*n))),
        Transform::PrependNumbers(n) => Ok(format!("{}{}", random_digits(*n), token)),
        Transform::AppendSymbols(n) => Ok(format!("{}{}", token, random_symbols(*n))),
        Transform::PrependSymbols(n) => Ok(format!("{}{}", random_symbols(*n), token)),
        Transform::Homoglyph => apply_homoglyph(token),
        Transform::HomoglyphRandom => apply_homoglyph_random(token),
        Transform::HomoglyphFull => apply_homoglyph_full(token),
        Transform::KeyboardShift => apply_keyboard_shift(token),
        Transform::PhoneticSubstitution => apply_phonetic_substitution(token),
        Transform::TransliterationLatin => apply_transliteration(token),
        Transform::DiacriticExpand => apply_diacritic_expand(token),
        Transform::DiacriticStrip => apply_diacritic_strip(token),
        Transform::EmojiInsertion => apply_emoji_insertion(token),
        Transform::EmojiRandom => apply_emoji_random(token),
        Transform::PluralizeEnd => Ok(pluralize(token)),
        Transform::SingularizeEnd => Ok(singularize(token)),
        Transform::DoubleLast => double_last_char(token),
        Transform::TripleLast => triple_last_char(token),
        Transform::ReverseWords => Ok(reverse_words(token)),
        Transform::InterleaveSpaces => Ok(interleave_spaces(token, " ")),
        Transform::RandomInsertSpaces => apply_random_insert_spaces(token),
        Transform::Custom(rule) => apply_custom_rule(token, rule),
    }
}

fn apply_leet_basic(token: &str) -> crate::Result<String> {
    let mut result = String::new();
    for ch in token.chars() {
        if let Some(replacements) = LEET_MAP.get(&ch.to_ascii_lowercase()) {
            result.push_str(replacements[0]);
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_leet_full(token: &str) -> crate::Result<String> {
    let mut result = String::new();
    for ch in token.chars() {
        if let Some(replacements) = LEET_MAP.get(&ch.to_ascii_lowercase()) {
            for replacement in replacements {
                result.push_str(replacement);
            }
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_leet_random(token: &str) -> crate::Result<String> {
    use rand::seq::SliceRandom;
    let mut rng = rand::thread_rng();
    let mut result = String::new();
    
    for ch in token.chars() {
        if let Some(replacements) = LEET_MAP.get(&ch.to_ascii_lowercase()) {
            if let Some(replacement) = replacements.choose(&mut rng) {
                result.push_str(replacement);
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_homoglyph(token: &str) -> crate::Result<String> {
    let mut result = String::new();
    for ch in token.chars() {
        if let Some(replacements) = HOMOGLYPH_MAP.get(&ch.to_ascii_lowercase()) {
            result.push_str(replacements[0]);
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_homoglyph_random(token: &str) -> crate::Result<String> {
    use rand::seq::SliceRandom;
    let mut rng = rand::thread_rng();
    let mut result = String::new();
    
    for ch in token.chars() {
        if let Some(replacements) = HOMOGLYPH_MAP.get(&ch.to_ascii_lowercase()) {
            if let Some(replacement) = replacements.choose(&mut rng) {
                result.push_str(replacement);
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_homoglyph_full(token: &str) -> crate::Result<String> {
    let mut result = String::new();
    for ch in token.chars() {
        result.push(ch);
        if let Some(replacements) = HOMOGLYPH_MAP.get(&ch.to_ascii_lowercase()) {
            for replacement in replacements {
                result.push_str(replacement);
            }
        }
    }
    Ok(result)
}

fn apply_keyboard_shift(token: &str) -> crate::Result<String> {
    use rand::seq::SliceRandom;
    let mut rng = rand::thread_rng();
    let mut result = String::new();
    
    for ch in token.chars() {
        if let Some(shifts) = KEYBOARD_SHIFT_MAP.get(&ch.to_ascii_lowercase()) {
            if let Some(shift) = shifts.choose(&mut rng) {
                result.push_str(shift);
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
        }
    }
    Ok(result)
}

fn apply_phonetic_substitution(token: &str) -> crate::Result<String> {
    let mut result = token.to_string();
    // Simple phonetic rules: ph->f, tion->sion, etc.
    result = result.replace("ph", "f");
    result = result.replace("tion", "sion");
    result = result.replace("ough", "uff");
    Ok(result)
}

fn apply_transliteration(token: &str) -> crate::Result<String> {
    // Use unidecode for basic transliteration
    Ok(unidecode::unidecode(token))
}

fn apply_diacritic_expand(token: &str) -> crate::Result<String> {
    let mut result = String::new();
    for ch in token.chars() {
        result.push(ch);
        if let Some(variants) = DIACRITIC_MAP.get(&ch.to_ascii_lowercase()) {
            for variant in variants {
                result.push_str(variant);
            }
        }
    }
    Ok(result)
}

fn apply_diacritic_strip(token: &str) -> crate::Result<String> {
    let normalized = unicode_normalization::UnicodeNormalization::nfd(token);
    let result: String = normalized
        .filter(|ch| !unicode_categories::is_mark_nonspacing(*ch))
        .collect();
    Ok(result)
}

fn apply_emoji_insertion(token: &str) -> crate::Result<String> {
    let emojis = ["😀", "🔥", "💯", "✨", "👍"];
    let pos = (token.len() / 2).min(token.len());
    let (left, right) = token.split_at(pos);
    Ok(format!("{}{}_{}", left, emojis[0], right))
}

fn apply_emoji_random(token: &str) -> crate::Result<String> {
    use rand::seq::SliceRandom;
    let mut rng = rand::thread_rng();
    let emojis = ["😀", "🔥", "💯", "✨", "👍", "❤️", "🎉", "🚀"];
    let pos = (token.len() / 2).min(token.len());
    let (left, right) = token.split_at(pos);
    if let Some(emoji) = emojis.choose(&mut rng) {
        Ok(format!("{}{}{}", left, emoji, right))
    } else {
        Ok(token.to_string())
    }
}

fn apply_random_insert_spaces(token: &str) -> crate::Result<String> {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    let mut result = String::new();
    
    for (i, ch) in token.chars().enumerate() {
        result.push(ch);
        if i < token.len() - 1 && rng.gen_bool(0.2) {
            result.push(' ');
        }
    }
    Ok(result)
}

fn apply_custom_rule(token: &str, rule: &str) -> crate::Result<String> {
    // Support simple pattern replacement: "find:replace"
    if let Some((find, replace)) = rule.split_once(':') {
        Ok(token.replace(find, replace))
    } else {
        Ok(token.to_string())
    }
}

fn toggle_case(s: &str) -> String {
    s.chars()
        .map(|c| {
            if c.is_uppercase() {
                c.to_lowercase().collect::<String>()
            } else {
                c.to_uppercase().collect::<String>()
            }
        })
        .collect()
}

fn capitalize(s: &str) -> String {
    let mut chars = s.chars();
    match chars.next() {
        None => String::new(),
        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
    }
}

fn to_title_case(s: &str) -> String {
    s.split_whitespace()
        .map(capitalize)
        .collect::<Vec<_>>()
        .join(" ")
}

fn pluralize(token: &str) -> String {
    if token.ends_with('y') {
        format!("{}ies", &token[..token.len() - 1])
    } else if token.ends_with('s') || token.ends_with('x') || token.ends_with('z') {
        format!("{}es", token)
    } else {
        format!("{}s", token)
    }
}

fn singularize(token: &str) -> String {
    if token.ends_with("ies") && token.len() > 3 {
        format!("{}y", &token[..token.len() - 3])
    } else if token.ends_with('s') && token.len() > 1 {
        token[..token.len() - 1].to_string()
    } else {
        token.to_string()
    }
}

fn double_last_char(token: &str) -> crate::Result<String> {
    if let Some(last) = token.chars().last() {
        Ok(format!("{}{}", token, last))
    } else {
        Ok(token.to_string())
    }
}

fn triple_last_char(token: &str) -> crate::Result<String> {
    if let Some(last) = token.chars().last() {
        Ok(format!("{}{}{}", token, last, last))
    } else {
        Ok(token.to_string())
    }
}

fn reverse_words(token: &str) -> String {
    token
        .split_whitespace()
        .rev()
        .collect::<Vec<_>>()
        .join(" ")
}

fn interleave_spaces(token: &str, sep: &str) -> String {
    token
        .chars()
        .map(|c| c.to_string())
        .collect::<Vec<_>>()
        .join(sep)
}

fn random_digits(n: usize) -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    (0..n)
        .map(|_| rng.gen_range(0..10).to_string())
        .collect::<String>()
}

fn random_symbols(n: usize) -> String {
    use rand::seq::SliceRandom;
    let mut rng = rand::thread_rng();
    let symbols = "!@#$%^&*";
    (0..n)
        .map(|_| {
            symbols
                .chars()
                .collect::<Vec<_>>()
                .choose(&mut rng)
                .unwrap()
                .to_string()
        })
        .collect::<String>()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_leet_basic() {
        let result = apply_leet_basic("password").unwrap();
        assert!(result.contains("p4ssword") || result.contains("p4ss0rd"));
    }

    #[test]
    fn test_capitalize() {
        assert_eq!(capitalize("hello"), "Hello");
    }

    #[test]
    fn test_reverse() {
        let result = apply_transform("hello", &Transform::Reverse).unwrap();
        assert_eq!(result, "olleh");
    }
}
