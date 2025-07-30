import pytest
from smart_chunker_engine.boundary_segmenter import BoundarySegmenter

def test_boundary_segmenter_smoke():
    """Smoke test for BoundarySegmenter instantiation and segment method signature."""
    segmenter = BoundarySegmenter()
    result = segmenter.segment(["token1", "token2", "token3"])
    assert isinstance(result, list) 