import pytest
from smart_chunker_engine.stats_gate import StatsGate
import numpy as np

def test_stats_gate_smoke():
    """Smoke test for StatsGate instantiation and should_enable method signature."""
    gate = StatsGate()
    result = gate.should_enable(["token1", "token2"])
    assert isinstance(result, (bool, np.bool_)) 