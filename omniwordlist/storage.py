"""
Storage and persistence layer

Handles checkpointing, output writing, compression, and metadata
"""

import gzip
import bz2
import json
from pathlib import Path
from typing import Iterator, Optional
from .error import StorageError


class OutputWriter:
    """Base output writer"""
    
    def __init__(self, path: Path, compression: Optional[str] = None, format: str = "txt"):
        """
        Initialize output writer
        
        Args:
            path: Output file path
            compression: Compression format (gzip, bzip2, lz4, zstd)
            format: Output format (txt, jsonl, csv)
        """
        self.path = path
        self.compression = compression
        self.format = format
        self.file_handle = None
        self.bytes_written = 0
        self.lines_written = 0
    
    def open(self):
        """Open output file"""
        # Ensure parent directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open with appropriate compression
        if self.compression == "gzip":
            self.file_handle = gzip.open(self.path, 'wt', encoding='utf-8')
        elif self.compression == "bzip2":
            self.file_handle = bz2.open(self.path, 'wt', encoding='utf-8')
        elif self.compression == "lz4":
            try:
                import lz4.frame
                self.file_handle = lz4.frame.open(self.path, 'wt', encoding='utf-8')
            except ImportError:
                raise StorageError("lz4 compression requires lz4 package")
        elif self.compression == "zstd":
            try:
                import zstandard as zstd
                cctx = zstd.ZstdCompressor()
                self.file_handle = cctx.stream_writer(open(self.path, 'wb'))
            except ImportError:
                raise StorageError("zstd compression requires zstandard package")
        else:
            self.file_handle = open(self.path, 'w', encoding='utf-8')
        
        # Write CSV header if needed
        if self.format == "csv":
            self._write_line("token,entropy,length")
    
    def write(self, token: str, metadata: dict = None):
        """
        Write a token to output
        
        Args:
            token: Token to write
            metadata: Optional metadata
        """
        if not self.file_handle:
            raise StorageError("Output file not opened")
        
        if self.format == "txt":
            line = token + "\n"
        elif self.format == "jsonl":
            from .filters import calculate_entropy
            data = {
                "token": token,
                "entropy": calculate_entropy(token),
                "length": len(token)
            }
            if metadata:
                data.update(metadata)
            line = json.dumps(data) + "\n"
        elif self.format == "csv":
            from .filters import calculate_entropy
            entropy = calculate_entropy(token)
            line = f'"{token}",{entropy},{len(token)}\n'
        else:
            line = token + "\n"
        
        self._write_line(line)
    
    def _write_line(self, line: str):
        """Internal method to write line"""
        if self.compression == "zstd":
            # zstd needs bytes
            self.file_handle.write(line.encode('utf-8'))
        else:
            self.file_handle.write(line)
        
        self.bytes_written += len(line.encode('utf-8'))
        self.lines_written += 1
    
    def close(self):
        """Close output file"""
        if self.file_handle:
            if self.compression == "zstd":
                # Flush zstd compressor
                try:
                    self.file_handle.flush()
                except:
                    pass
            self.file_handle.close()
            self.file_handle = None
    
    def __enter__(self):
        """Context manager entry"""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class CheckpointManager:
    """Manage generation checkpoints for resume capability"""
    
    def __init__(self, checkpoint_dir: Path):
        """
        Initialize checkpoint manager
        
        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(self, job_id: str, state: dict):
        """
        Save checkpoint state
        
        Args:
            job_id: Job identifier
            state: State dictionary to save
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_checkpoint(self, job_id: str) -> Optional[dict]:
        """
        Load checkpoint state
        
        Args:
            job_id: Job identifier
            
        Returns:
            State dictionary or None
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        if not checkpoint_path.exists():
            return None
        
        with open(checkpoint_path, 'r') as f:
            return json.load(f)
    
    def delete_checkpoint(self, job_id: str):
        """
        Delete checkpoint
        
        Args:
            job_id: Job identifier
        """
        checkpoint_path = self.checkpoint_dir / f"{job_id}.checkpoint.json"
        if checkpoint_path.exists():
            checkpoint_path.unlink()


def write_tokens_to_file(tokens: Iterator[str], output_path: Path, 
                        compression: Optional[str] = None, 
                        format: str = "txt") -> int:
    """
    Write tokens to file with optional compression
    
    Args:
        tokens: Iterator of tokens
        output_path: Output file path
        compression: Optional compression format
        format: Output format
        
    Returns:
        Number of tokens written
    """
    count = 0
    with OutputWriter(output_path, compression, format) as writer:
        for token in tokens:
            writer.write(token)
            count += 1
    return count
