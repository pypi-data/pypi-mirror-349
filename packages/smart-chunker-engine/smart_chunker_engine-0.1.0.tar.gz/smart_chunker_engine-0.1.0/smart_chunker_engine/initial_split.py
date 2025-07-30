from typing import Optional, List, Dict, Any
from chunk_metadata_adapter.models import SemanticChunk
from chunk_metadata_adapter import ChunkType
import uuid
import hashlib

class InitialSplitter:
    """Splits normalized text into fixed or hybrid-length SemanticChunks."""

    def __init__(self, chunk_size: int = 500, overlap: int = 0, config: Optional[Dict[str, Any]] = None):
        """Initialize InitialSplitter with chunk size, overlap, and optional config.

        Args:
            chunk_size (int): Target chunk size in characters.
            overlap (int): Overlap size in characters between chunks.
            config (Optional[Dict[str, Any]]): Optional configuration dict.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.language = 'ru'
        self.chunk_type = ChunkType.DOC_BLOCK
        if config:
            self.chunk_size = config.get('chunk_size', self.chunk_size)
            self.overlap = config.get('overlap', self.overlap)
            self.language = config.get('language', self.language)
            self.chunk_type = config.get('chunk_type', self.chunk_type)

    def split(self, text: str) -> List[SemanticChunk]:
        """Split text into SemanticChunks of specified size.

        Args:
            text (str): Normalized input text.
        Returns:
            List[SemanticChunk]: List of SemanticChunk objects with metadata.
        """
        if not text or self.chunk_size <= 0:
            return []
        chunks = []
        start = 0
        text_len = len(text)
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk_text = text[start:end]
            chunk_uuid = str(uuid.uuid4())
            chunk_sha256 = hashlib.sha256(chunk_text.encode('utf-8')).hexdigest()
            chunk = SemanticChunk(
                uuid=chunk_uuid,
                type=self.chunk_type,
                text=chunk_text,
                language=self.language,
                sha256=chunk_sha256
            )
            chunks.append(chunk)
            if self.overlap > 0:
                start += self.chunk_size - self.overlap
                if start <= 0:
                    start = end  # fallback to non-overlapping if overlap is too big
            else:
                start = end
        return chunks 