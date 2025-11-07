/// Storage and persistence layer
/// 
/// Handles checkpointing, output writing, compression, and metadata

use std::fs::File;
use std::io::{Write, BufWriter};
use std::path::Path;
use chrono::Local;

pub struct StorageWriter {
    output_path: std::path::PathBuf,
    compression: Option<String>,
    buffer_size: usize,
}

impl StorageWriter {
    pub fn new(output_path: impl AsRef<Path>, compression: Option<String>) -> Self {
        Self {
            output_path: output_path.as_ref().to_path_buf(),
            compression,
            buffer_size: 8192,
        }
    }

    /// Write tokens to file
    pub fn write_tokens(&self, tokens: &[String]) -> crate::Result<()> {
        // Create output directory if needed
        if let Some(parent) = self.output_path.parent() {
            std::fs::create_dir_all(parent)?;
        }

        let file = File::create(&self.output_path)?;
        let mut writer = BufWriter::with_capacity(self.buffer_size, file);

        match self.compression.as_deref() {
            Some("gzip") => self.write_gzipped(&mut writer, tokens)?,
            Some("bzip2") => self.write_bzip2(&mut writer, tokens)?,
            Some("lz4") => self.write_lz4(&mut writer, tokens)?,
            Some("zstd") => self.write_zstd(&mut writer, tokens)?,
            None => self.write_plain(&mut writer, tokens)?,
            Some(fmt) => return Err(crate::Error::StorageError(
                format!("Unsupported compression: {}", fmt)
            )),
        }

        writer.flush()?;
        Ok(())
    }

    fn write_plain(&self, writer: &mut BufWriter<File>, tokens: &[String]) -> crate::Result<()> {
        for token in tokens {
            writeln!(writer, "{}", token)?;
        }
        Ok(())
    }

    fn write_gzipped(&self, writer: &mut BufWriter<File>, tokens: &[String]) -> crate::Result<()> {
        use flate2::Compression;
        use flate2::write::GzEncoder;

        let mut encoder = GzEncoder::new(writer, Compression::best());
        for token in tokens {
            writeln!(encoder, "{}", token)?;
        }
        encoder.finish()?;
        Ok(())
    }

    fn write_bzip2(&self, writer: &mut BufWriter<File>, tokens: &[String]) -> crate::Result<()> {
        use bzip2::write::BzEncoder;
        use bzip2::Compression;

        let mut encoder = BzEncoder::new(writer, Compression::best());
        for token in tokens {
            writeln!(encoder, "{}", token)?;
        }
        encoder.finish()?;
        Ok(())
    }

    fn write_lz4(&self, writer: &mut BufWriter<File>, tokens: &[String]) -> crate::Result<()> {
        use lz4_flex::frame::FrameEncoder;

        let mut encoder = FrameEncoder::new(writer);
        for token in tokens {
            writeln!(encoder, "{}", token)?;
        }
        encoder.finish()?;
        Ok(())
    }

    fn write_zstd(&self, writer: &mut BufWriter<File>, tokens: &[String]) -> crate::Result<()> {
        use zstd::stream::write::Encoder;

        let mut encoder = Encoder::new(writer, 21)?;
        for token in tokens {
            writeln!(encoder, "{}", token)?;
        }
        encoder.finish()?;
        Ok(())
    }

    /// Write JSONL format
    pub fn write_jsonl(&self, tokens: &[String]) -> crate::Result<()> {
        if let Some(parent) = self.output_path.parent() {
            std::fs::create_dir_all(parent)?;
        }

        let file = File::create(&self.output_path)?;
        let mut writer = BufWriter::with_capacity(self.buffer_size, file);

        for token in tokens {
            let json = serde_json::json!({ "token": token });
            writeln!(writer, "{}", json)?;
        }

        writer.flush()?;
        Ok(())
    }

    /// Write CSV format
    pub fn write_csv(&self, tokens: &[String]) -> crate::Result<()> {
        if let Some(parent) = self.output_path.parent() {
            std::fs::create_dir_all(parent)?;
        }

        let file = File::create(&self.output_path)?;
        let mut writer = BufWriter::with_capacity(self.buffer_size, file);

        writeln!(writer, "token,length,entropy")?;
        
        for token in tokens {
            let entropy = crate::filters::calculate_entropy(token);
            writeln!(writer, "\"{}\",{},{:.2}", token, token.len(), entropy)?;
        }

        writer.flush()?;
        Ok(())
    }
}

/// Checkpoint manager for resumable generation
pub struct CheckpointManager {
    checkpoint_dir: std::path::PathBuf,
}

impl CheckpointManager {
    pub fn new(checkpoint_dir: impl AsRef<Path>) -> crate::Result<Self> {
        let dir = checkpoint_dir.as_ref();
        std::fs::create_dir_all(dir)?;
        Ok(Self {
            checkpoint_dir: dir.to_path_buf(),
        })
    }

    /// Save checkpoint
    pub fn save_checkpoint(
        &self,
        job_id: &str,
        state: &CheckpointState,
    ) -> crate::Result<()> {
        let path = self.checkpoint_dir.join(format!("{}.json", job_id));
        let json = serde_json::to_string_pretty(state)?;
        std::fs::write(path, json)?;
        Ok(())
    }

    /// Load checkpoint
    pub fn load_checkpoint(&self, job_id: &str) -> crate::Result<Option<CheckpointState>> {
        let path = self.checkpoint_dir.join(format!("{}.json", job_id));
        if !path.exists() {
            return Ok(None);
        }

        let content = std::fs::read_to_string(&path)?;
        let state = serde_json::from_str(&content)?;
        Ok(Some(state))
    }

    /// List all checkpoints
    pub fn list_checkpoints(&self) -> crate::Result<Vec<String>> {
        let mut checkpoints = Vec::new();
        for entry in std::fs::read_dir(&self.checkpoint_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("json") {
                if let Some(name) = path.file_stem().and_then(|s| s.to_str()) {
                    checkpoints.push(name.to_string());
                }
            }
        }
        Ok(checkpoints)
    }

    /// Delete checkpoint
    pub fn delete_checkpoint(&self, job_id: &str) -> crate::Result<()> {
        let path = self.checkpoint_dir.join(format!("{}.json", job_id));
        if path.exists() {
            std::fs::remove_file(path)?;
        }
        Ok(())
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct CheckpointState {
    pub job_id: String,
    pub timestamp: String,
    pub config: crate::Config,
    pub last_token: Option<String>,
    pub tokens_generated: u64,
    pub current_length: usize,
    pub start_index: usize,
}

impl CheckpointState {
    pub fn new(job_id: String, config: crate::Config) -> Self {
        Self {
            job_id,
            timestamp: Local::now().to_rfc3339(),
            config,
            last_token: None,
            tokens_generated: 0,
            current_length: 0,
            start_index: 0,
        }
    }

    pub fn update(&mut self, token: &str, index: usize) {
        self.last_token = Some(token.to_string());
        self.tokens_generated += 1;
        self.start_index = index;
        self.timestamp = Local::now().to_rfc3339();
    }
}

/// Job metadata
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct JobMetadata {
    pub job_id: String,
    pub created_at: String,
    pub config: crate::Config,
    pub status: JobStatus,
    pub tokens_count: u64,
    pub output_file: Option<std::path::PathBuf>,
    pub estimated_cardinality: u64,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub enum JobStatus {
    Pending,
    Running,
    Completed,
    Failed(String),
    Paused,
}

pub struct JobManager {
    jobs_dir: std::path::PathBuf,
}

impl JobManager {
    pub fn new(jobs_dir: impl AsRef<Path>) -> crate::Result<Self> {
        let dir = jobs_dir.as_ref();
        std::fs::create_dir_all(dir)?;
        Ok(Self {
            jobs_dir: dir.to_path_buf(),
        })
    }

    /// Save job metadata
    pub fn save_job(&self, job: &JobMetadata) -> crate::Result<()> {
        let path = self.jobs_dir.join(format!("{}.json", job.job_id));
        let json = serde_json::to_string_pretty(job)?;
        std::fs::write(path, json)?;
        Ok(())
    }

    /// Load job metadata
    pub fn load_job(&self, job_id: &str) -> crate::Result<Option<JobMetadata>> {
        let path = self.jobs_dir.join(format!("{}.json", job_id));
        if !path.exists() {
            return Ok(None);
        }

        let content = std::fs::read_to_string(&path)?;
        let job = serde_json::from_str(&content)?;
        Ok(Some(job))
    }

    /// List all jobs
    pub fn list_jobs(&self) -> crate::Result<Vec<JobMetadata>> {
        let mut jobs = Vec::new();
        for entry in std::fs::read_dir(&self.jobs_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("json") {
                if let Ok(content) = std::fs::read_to_string(&path) {
                    if let Ok(job) = serde_json::from_str(&content) {
                        jobs.push(job);
                    }
                }
            }
        }
        Ok(jobs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn test_storage_writer() -> crate::Result<()> {
        let temp_dir = TempDir::new()?;
        let output_path = temp_dir.path().join("test.txt");
        let writer = StorageWriter::new(&output_path, None);
        
        let tokens = vec!["hello".to_string(), "world".to_string()];
        writer.write_tokens(&tokens)?;
        
        let content = std::fs::read_to_string(&output_path)?;
        assert!(content.contains("hello"));
        assert!(content.contains("world"));
        
        Ok(())
    }

    #[test]
    fn test_checkpoint_manager() -> crate::Result<()> {
        let temp_dir = TempDir::new()?;
        let manager = CheckpointManager::new(temp_dir.path())?;
        
        let mut state = CheckpointState::new("test_job".to_string(), crate::Config::default());
        state.update("token1", 0);
        
        manager.save_checkpoint("test_job", &state)?;
        let loaded = manager.load_checkpoint("test_job")?;
        
        assert!(loaded.is_some());
        let loaded_state = loaded.unwrap();
        assert_eq!(loaded_state.job_id, "test_job");
        
        Ok(())
    }
}
