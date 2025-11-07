use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("IO Error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Configuration error: {0}")]
    ConfigError(String),

    #[error("Generator error: {0}")]
    GeneratorError(String),

    #[error("Transform error: {0}")]
    TransformError(String),

    #[error("Storage error: {0}")]
    StorageError(String),

    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),

    #[error("Database error: {0}")]
    DatabaseError(#[from] rusqlite::Error),

    #[error("Invalid charset: {0}")]
    InvalidCharset(String),

    #[error("Field error: {0}")]
    FieldError(String),

    #[error("Preset error: {0}")]
    PresetError(String),

    #[error("Regex error: {0}")]
    RegexError(#[from] regex::Error),

    #[error("UTF-8 error: {0}")]
    Utf8Error(#[from] std::string::FromUtf8Error),

    #[error("Anyhow: {0}")]
    Other(#[from] anyhow::Error),
}

pub type Result<T> = std::result::Result<T, Error>;
