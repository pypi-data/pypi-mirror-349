import pytest
from smart_chunker_engine.tfidf_layer import TfidfLayer

def test_tfidf_layer_smoke():
    """Smoke test for TfidfLayer instantiation and compute method signature."""
    layer = TfidfLayer()
    result = layer.compute(["token1", "token2"], {"token1": 1.0, "token2": 2.0})
    assert isinstance(result, dict) 