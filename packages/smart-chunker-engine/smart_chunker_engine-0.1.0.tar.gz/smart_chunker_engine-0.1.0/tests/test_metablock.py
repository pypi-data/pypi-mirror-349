import pytest
from smart_chunker_engine.metablock import MetablockSegmenter

def test_metablock_segmenter_smoke():
    """Smoke test for MetablockSegmenter instantiation and split method signature."""
    segmenter = MetablockSegmenter()
    result = segmenter.split([{"text": "chunk1"}, {"text": "chunk2"}])
    assert isinstance(result, list) 