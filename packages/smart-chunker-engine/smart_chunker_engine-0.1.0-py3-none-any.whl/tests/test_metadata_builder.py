import pytest
from smart_chunker_engine.metadata_builder import MetadataBuilder
from chunk_metadata_adapter import SemanticChunk, FlatSemanticChunk, ChunkMetrics

def test_build_semantic_chunk_basic():
    chunk = MetadataBuilder.build_semantic_chunk(
        text="test text",
        start=0,
        end=9,
        method="hybrid",
        cohesion=0.5,
        boundary_prev=0.7,
        boundary_next=0.6,
        coverage=0.8,
        tags=["t1"],
        language="ru",
        type="DocBlock"
    )
    assert isinstance(chunk, SemanticChunk)
    assert chunk.metrics.cohesion == 0.5
    assert chunk.metrics.boundary_prev == 0.7
    assert chunk.metrics.boundary_next == 0.6
    assert chunk.metrics.coverage == 0.8
    assert chunk.tags == ["t1"]
    assert chunk.language == "ru"
    assert chunk.type == "DocBlock"
    assert isinstance(chunk.uuid, str) and len(chunk.uuid) > 0
    import hashlib
    assert chunk.sha256 == hashlib.sha256("test text".encode()).hexdigest()

def test_build_semantic_chunk_with_metrics():
    metrics = ChunkMetrics(cohesion=0.1, boundary_prev=0.2, boundary_next=0.3, coverage=0.4)
    chunk = MetadataBuilder.build_semantic_chunk(
        text="abc",
        start=1,
        end=4,
        method="fixed",
        metrics=metrics,
        language="ru",
        type="DocBlock"
    )
    assert chunk.metrics.cohesion == 0.1
    assert chunk.metrics.boundary_prev == 0.2
    assert chunk.metrics.boundary_next == 0.3
    assert chunk.metrics.coverage == 0.4
    assert chunk.language == "ru"
    assert chunk.type == "DocBlock"
    assert isinstance(chunk.uuid, str) and len(chunk.uuid) > 0
    import hashlib
    assert chunk.sha256 == hashlib.sha256("abc".encode()).hexdigest()

def test_build_flat_metadata_from_semantic():
    chunk = MetadataBuilder.build_semantic_chunk(
        text="flat",
        start=0,
        end=4,
        method="hybrid",
        cohesion=0.9,
        boundary_prev=0.8,
        boundary_next=0.7,
        coverage=0.6,
        language="ru",
        type="DocBlock"
    )
    flat = MetadataBuilder.build_flat_metadata(chunk)
    assert isinstance(flat, FlatSemanticChunk)
    assert flat.cohesion == 0.9
    assert flat.boundary_prev == 0.8
    assert flat.boundary_next == 0.7
    assert flat.coverage == 0.6
    assert flat.language == "ru"
    assert flat.type == "DocBlock"
    assert isinstance(flat.uuid, str) and len(flat.uuid) > 0
    import hashlib
    assert flat.sha256 == hashlib.sha256("flat".encode()).hexdigest()

def test_build_flat_metadata_override():
    chunk = MetadataBuilder.build_semantic_chunk(
        text="flat2",
        start=0,
        end=5,
        method="hybrid",
        cohesion=0.1,
        boundary_prev=0.2,
        boundary_next=0.3,
        coverage=0.4,
        language="ru",
        type="DocBlock"
    )
    flat = MetadataBuilder.build_flat_metadata(chunk, cohesion=0.5, boundary_prev=0.6, boundary_next=0.7, coverage=0.8)
    assert flat.cohesion == 0.5
    assert flat.boundary_prev == 0.6
    assert flat.boundary_next == 0.7
    assert flat.coverage == 0.8
    assert flat.language == "ru"
    assert flat.type == "DocBlock"
    assert isinstance(flat.uuid, str) and len(flat.uuid) > 0
    import hashlib
    assert flat.sha256 == hashlib.sha256("flat2".encode()).hexdigest()

def test_build_flat_metadata_from_dict():
    chunk = MetadataBuilder.build_semantic_chunk(
        text="dict",
        start=0,
        end=4,
        method="hybrid",
        cohesion=0.2,
        boundary_prev=0.3,
        boundary_next=0.4,
        coverage=0.5,
        language="ru",
        type="DocBlock"
    )
    chunk_dict = chunk.model_dump()
    flat = MetadataBuilder.build_flat_metadata(chunk_dict)
    assert isinstance(flat, FlatSemanticChunk)
    assert flat.cohesion == 0.2
    assert flat.boundary_prev == 0.3
    assert flat.boundary_next == 0.4
    assert flat.coverage == 0.5
    assert flat.language == "ru"
    assert flat.type == "DocBlock"
    assert isinstance(flat.uuid, str) and len(flat.uuid) > 0
    import hashlib
    assert flat.sha256 == hashlib.sha256("dict".encode()).hexdigest()

def test_from_flat_roundtrip():
    chunk = MetadataBuilder.build_semantic_chunk(
        text="round",
        start=0,
        end=5,
        method="hybrid",
        cohesion=0.11,
        boundary_prev=0.22,
        boundary_next=0.33,
        coverage=0.44,
        language="ru",
        type="DocBlock"
    )
    flat = MetadataBuilder.build_flat_metadata(chunk)
    restored = MetadataBuilder.from_flat(flat)
    assert isinstance(restored, SemanticChunk)
    assert restored.metrics.cohesion == 0.11
    assert restored.metrics.boundary_prev == 0.22
    assert restored.metrics.boundary_next == 0.33
    assert restored.metrics.coverage == 0.44
    assert restored.language == "ru"
    assert restored.type == "DocBlock"
    assert isinstance(restored.uuid, str) and len(restored.uuid) > 0
    import hashlib
    assert restored.sha256 == hashlib.sha256("round".encode()).hexdigest()

def test_validate_metrics_valid():
    # All valid
    MetadataBuilder.validate_metrics(cohesion=0.0, boundary_prev=0.5, boundary_next=1.0, coverage=0.99)
    # All None
    MetadataBuilder.validate_metrics()
    # Some None
    MetadataBuilder.validate_metrics(cohesion=None, boundary_prev=0.1)

def test_validate_metrics_invalid():
    with pytest.raises(ValueError):
        MetadataBuilder.validate_metrics(cohesion=-0.1)
    with pytest.raises(ValueError):
        MetadataBuilder.validate_metrics(boundary_prev=1.1)
    with pytest.raises(ValueError):
        MetadataBuilder.validate_metrics(boundary_next=2)
    with pytest.raises(ValueError):
        MetadataBuilder.validate_metrics(coverage=-0.01)

def test_export_semantic_and_flat(tmp_path):
    from smart_chunker_engine.exporter import export_chunks
    chunk = MetadataBuilder.build_semantic_chunk(
        text="export test",
        start=0,
        end=11,
        method="hybrid",
        cohesion=0.5,
        boundary_prev=0.6,
        boundary_next=0.7,
        coverage=0.8,
        language="ru",
        type="DocBlock"
    )
    flat = MetadataBuilder.build_flat_metadata(chunk)
    # Export SemanticChunk to JSON
    json_path = tmp_path / "semantic_chunks.json"
    export_chunks([chunk], json_path, format="json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = f.read()
    assert "export test" in data
    # Export FlatSemanticChunk to CSV
    csv_path = tmp_path / "flat_chunks.csv"
    export_chunks([flat], csv_path, format="csv")
    with open(csv_path, "r", encoding="utf-8") as f:
        header = f.readline()
        row = f.readline()
    assert "export test" in row 