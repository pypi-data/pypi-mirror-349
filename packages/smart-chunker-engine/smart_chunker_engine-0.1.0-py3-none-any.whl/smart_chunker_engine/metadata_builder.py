from chunk_metadata_adapter import SemanticChunk, FlatSemanticChunk, ChunkMetrics
from typing import Optional, List, Dict, Any, Union
import uuid as _uuid
import hashlib

class MetadataBuilder:
    """Builder for SemanticChunk and FlatSemanticChunk metadata objects.

    Provides methods to construct and convert chunk metadata using chunk_metadata_adapter models.
    """

    @staticmethod
    def build_semantic_chunk(
        text: str,
        start: int,
        end: int,
        method: str,
        status: str = "RAW",
        metrics: Optional[ChunkMetrics] = None,
        cohesion: Optional[float] = None,
        boundary_prev: Optional[float] = None,
        boundary_next: Optional[float] = None,
        coverage: Optional[float] = None,
        tags: Optional[List[str]] = None,
        uuid: Optional[str] = None,
        type: str = "DocBlock",
        language: str = "ru",
        sha256: Optional[str] = None,
    ) -> SemanticChunk:
        """Builds a SemanticChunk object with extended metrics and all required fields.

        Args:
            text: Chunk text.
            start: Start byte offset.
            end: End byte offset.
            method: Segmentation method.
            status: Chunk status (RAW/RELIABLE/VALIDATED/REJECTED).
            metrics: Optional ChunkMetrics object.
            cohesion: Optional cohesion metric (0..1).
            boundary_prev: Optional previous boundary metric (0..1).
            boundary_next: Optional next boundary metric (0..1).
            coverage: Optional coverage metric (0..1).
            tags: Optional list of tags.
            uuid: Optional unique uuid (if None, generated).
            type: Chunk type (default 'DocBlock', must be valid Enum value).
            language: Language code (default 'ru').
            sha256: Optional SHA-256 hash of text (if None, computed).
        Returns:
            SemanticChunk: Metadata object.
        """
        if metrics is None:
            metrics = ChunkMetrics(
                cohesion=cohesion,
                boundary_prev=boundary_prev,
                boundary_next=boundary_next,
                coverage=coverage
            )
        if uuid is None:
            uuid = str(_uuid.uuid4())
        if sha256 is None:
            sha256 = hashlib.sha256(text.encode()).hexdigest()
        return SemanticChunk(
            uuid=uuid,
            text=text,
            start=start,
            end=end,
            method=method,
            status=status,
            metrics=metrics,
            tags=tags or [],
            type=type,
            language=language,
            sha256=sha256
        )

    @staticmethod
    def build_flat_metadata(
        chunk: Union[SemanticChunk, Dict[str, Any]],
        coverage: Optional[float] = None,
        cohesion: Optional[float] = None,
        boundary_prev: Optional[float] = None,
        boundary_next: Optional[float] = None,
    ) -> FlatSemanticChunk:
        """Converts a SemanticChunk (or dict) to FlatSemanticChunk, mapping extended metrics.

        Args:
            chunk: SemanticChunk object or dict.
            coverage: Optional coverage metric (overrides chunk.metrics.coverage).
            cohesion: Optional cohesion metric (overrides chunk.metrics.cohesion).
            boundary_prev: Optional previous boundary metric (overrides chunk.metrics.boundary_prev).
            boundary_next: Optional next boundary metric (overrides chunk.metrics.boundary_next).
        Returns:
            FlatSemanticChunk: Flat metadata object.
        """
        if isinstance(chunk, dict):
            chunk = SemanticChunk(**chunk)
        flat = FlatSemanticChunk.from_semantic_chunk(chunk)
        # Patch extended metrics if provided
        if coverage is not None:
            flat.coverage = coverage
        if cohesion is not None:
            flat.cohesion = cohesion
        if boundary_prev is not None:
            flat.boundary_prev = boundary_prev
        if boundary_next is not None:
            flat.boundary_next = boundary_next
        return flat

    @staticmethod
    def from_flat(flat: FlatSemanticChunk) -> SemanticChunk:
        """Converts a FlatSemanticChunk back to SemanticChunk, restoring extended metrics.

        Args:
            flat: FlatSemanticChunk object.
        Returns:
            SemanticChunk: Restored metadata object.
        """
        return flat.to_semantic_chunk()

    @staticmethod
    def validate_metrics(
        cohesion: Optional[float] = None,
        boundary_prev: Optional[float] = None,
        boundary_next: Optional[float] = None,
        coverage: Optional[float] = None,
    ) -> None:
        """Validates that all metrics are in [0, 1] or None.

        Args:
            cohesion: Cohesion metric.
            boundary_prev: Previous boundary metric.
            boundary_next: Next boundary metric.
            coverage: Coverage metric.
        Raises:
            ValueError: If any metric is not None and not in [0, 1].
        """
        for name, value in [
            ("cohesion", cohesion),
            ("boundary_prev", boundary_prev),
            ("boundary_next", boundary_next),
            ("coverage", coverage),
        ]:
            if value is not None and not (0.0 <= value <= 1.0):
                raise ValueError(f"Metric '{name}' must be in [0, 1], got {value}") 