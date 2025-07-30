import pytest
from smart_chunker_engine.pipeline import SmartChunkerPipeline
from chunk_metadata_adapter import SemanticChunk
from smart_chunker_engine.exporter import export_chunks
import tempfile
import os

def test_pipeline_basic():
    text = "Это пример текста для тестирования пайплайна. Он содержит несколько предложений. Проверяем разбиение и метаданные."
    config = {'split': {'chunk_size': 40}}
    pipeline = SmartChunkerPipeline(config)
    chunks = pipeline.run(text)
    assert isinstance(chunks, list)
    assert all(isinstance(c, SemanticChunk) for c in chunks)
    assert len(chunks) > 0
    # Проверяем, что покрытие текста есть
    total_text = "".join([c.text for c in chunks])
    assert set(total_text.replace(" ", "")) <= set(text.replace(" ", ""))
    # Проверяем экспорт
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "chunks.json")
        export_chunks(chunks, out_path, format="json")
        assert os.path.exists(out_path) 