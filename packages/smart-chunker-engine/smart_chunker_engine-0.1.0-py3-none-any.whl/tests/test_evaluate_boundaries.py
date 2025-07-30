import subprocess
import json
from pathlib import Path

def test_evaluate_boundaries(tmp_path):
    # Prepare dummy chunk and gold files
    chunks = [0, 40, 90, 150]
    gold = [0, 40, 90, 150]
    chunks_path = tmp_path / "chunks.json"
    gold_path = tmp_path / "gold.json"
    report_path = tmp_path / "report.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f)
    with open(gold_path, "w", encoding="utf-8") as f:
        json.dump(gold, f)
    # Run script
    result = subprocess.run([
        "python3", "scripts/evaluate_boundaries.py",
        "--chunks", str(chunks_path),
        "--gold", str(gold_path),
        "--output", str(report_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    with open(report_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    assert metrics["f1"] >= 0.90
    assert metrics["noise_rate"] <= 3.0
    assert metrics["cv"] <= 30.0 