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

    #[error("LZ4 compression error: {0}")]
    Lz4Error(String),

    #[error("TOML serialization error: {0}")]
    TomlSerError(String),
}

impl From<lz4_flex::frame::Error> for Error {
    fn from(err: lz4_flex::frame::Error) -> Self {
        Error::Lz4Error(err.to_string())
    }
}

impl From<toml::ser::Error> for Error {
    fn from(err: toml::ser::Error) -> Self {
        Error::TomlSerError(err.to_string())
    }
}

pub type Result<T> = std::result::Result<T, Error>;
