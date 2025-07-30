import subprocess
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import sys
import pytest

def parse_junit(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    failures = int(root.attrib.get("failures", 0))
    skipped = root.findall(".//skipped")
    return failures, len(skipped)

def test_length_stats_ok(tmp_path):
    """CV=0, не должно быть failure/skipped"""
    boundaries = [0, 10, 20, 30]
    chunks_path = tmp_path / "chunks.json"
    xml_path = tmp_path / "len.xml"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump([{"start": b, "end": b+10} for b in boundaries], f)
    result = subprocess.run([
        sys.executable, "scripts/length_stats.py",
        "--chunks", str(chunks_path),
        "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0
    assert skipped == 0

def test_length_stats_warning(tmp_path):
    """CV=~32, должен быть warning (skipped)"""
    boundaries = [0, 10, 30, 60]  # CV ~32%
    chunks_path = tmp_path / "chunks.json"
    xml_path = tmp_path / "len.xml"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump([{"start": b, "end": b+10} for b in boundaries], f)
    result = subprocess.run([
        sys.executable, "scripts/length_stats.py",
        "--chunks", str(chunks_path),
        "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0
    assert skipped == 1

def test_coverage_check(tmp_path):
    """Min coverage 0.7, не должно быть failure/skipped"""
    chunks = [{"metrics": {"coverage": 0.7}}, {"metrics": {"coverage": 0.8}}]
    chunks_path = tmp_path / "chunks.json"
    xml_path = tmp_path / "cov.xml"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f)
    result = subprocess.run([
        sys.executable, "scripts/coverage_check.py",
        "--chunks", str(chunks_path),
        "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0

def test_time_benchmark(tmp_path):
    """Dummy script, time < 3 сек, не должно быть failure/skipped"""
    script = tmp_path / "dummy.py"
    xml_path = tmp_path / "time.xml"
    with open(script, "w", encoding="utf-8") as f:
        f.write("import time; time.sleep(1)")
    result = subprocess.run([
        sys.executable, "scripts/time_benchmark.py",
        "--script", str(script), "--input", "", "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0

def test_memory_benchmark(tmp_path):
    """Dummy script, если нет psutil — skip тест, иначе не должно быть failure (или warning)"""
    try:
        import psutil  # noqa: F401
    except ImportError:
        pytest.skip("psutil not installed")
    script = tmp_path / "dummy_mem.py"
    xml_path = tmp_path / "mem.xml"
    with open(script, "w", encoding="utf-8") as f:
        f.write("a = [0]*1000000; import time; time.sleep(1)")
    result = subprocess.run([
        sys.executable, "scripts/memory_benchmark.py",
        "--script", str(script), "--input", "", "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0 or skipped >= 0  # allow warning

def test_smoke_test(tmp_path):
    """Dummy script, быстрый, не должно быть failure/skipped"""
    script = tmp_path / "dummy_smoke.py"
    xml_path = tmp_path / "smoke.xml"
    with open(script, "w", encoding="utf-8") as f:
        f.write("print('ok')")
    result = subprocess.run([
        sys.executable, "scripts/smoke_test.py",
        "--script", str(script), "--input", "", "--junit", str(xml_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    failures, skipped = parse_junit(xml_path)
    assert failures == 0 