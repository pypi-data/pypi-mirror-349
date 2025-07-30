import numpy as np
from smart_chunker_engine import metrics

def test_cohesion_pairwise():
    """Test cohesion for two identical and two orthogonal vectors."""
    v1 = np.array([1.0, 0.0])
    v2 = np.array([1.0, 0.0])
    v3 = np.array([0.0, 1.0])
    assert metrics.cohesion([v1, v2]) == 1.0
    assert np.isclose(metrics.cohesion([v1, v3]), 0.0)

def test_boundary():
    """Test boundary metric for identical and orthogonal vectors."""
    v1 = np.array([1.0, 0.0])
    v2 = np.array([1.0, 0.0])
    v3 = np.array([0.0, 1.0])
    assert metrics.boundary(v1, v2) == 1.0
    assert np.isclose(metrics.boundary(v1, v3), 0.0)

def test_coverage():
    """Test coverage metric (should match boundary for same vectors)."""
    v1 = np.array([1.0, 0.0])
    v2 = np.array([1.0, 0.0])
    assert metrics.coverage(v1, v2) == 1.0

def test_off_topic():
    """Test off_topic tag logic."""
    assert metrics.off_topic(0.5, threshold=0.6)
    assert not metrics.off_topic(0.7, threshold=0.6)

def test_boundary_metrics():
    """Test boundary_prev/next computation for a sequence of vectors."""
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.0, 1.0])
    v3 = np.array([1.0, 0.0])
    out = metrics.boundary_metrics([v1, v2, v3])
    assert out[0]['boundary_prev'] is None
    assert out[0]['boundary_next'] is not None
    assert out[-1]['boundary_next'] is None 