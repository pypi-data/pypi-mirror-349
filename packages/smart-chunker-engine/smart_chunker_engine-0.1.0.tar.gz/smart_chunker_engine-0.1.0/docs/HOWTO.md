# Smart Chunker Engine: HOWTO / Практические инструкции

## 1. Быстрый старт / Quick Start
```python
from smart_chunker_engine.pipeline import SmartChunkerPipeline
from smart_chunker_engine.exporter import export_chunks

text = "Ваш текст..."
pipeline = SmartChunkerPipeline()
chunks = pipeline.run(text)
export_chunks(chunks, "output.json", format="json")
```

## 2. Настройка параметров / Custom Configuration
```python
config = {
    'split': {'chunk_size': 300, 'overlap': 20},
    'boundary': {'window_size': 15, 'threshold': 0.12},
    'stats_gate': {'var_thr': 0.1},
    'triple_cluster': {'min_cluster': 3},
    'tfidf': {'top_n': 200},
    'iter_refine': {'lambda_': 0.3, 'max_iter': 2}
}
pipeline = SmartChunkerPipeline(config)
chunks = pipeline.run(text)
```

## 3. Экспорт результата / Exporting Results
```python
from smart_chunker_engine.exporter import export_chunks
export_chunks(chunks, "output.json", format="json")
export_chunks(chunks, "output.csv", format="csv")  # FlatSemanticChunk only
```

## 4. Оценка качества / Quality Evaluation
```bash
python scripts/evaluate_boundaries.py --chunks my_chunks.json --gold gold.json --output report.json
cat report.json
```

## 5. Интеграция в проект / Integration
- Добавьте smart_chunker_engine и chunk_metadata_adapter в зависимости.
- Импортируйте SmartChunkerPipeline, используйте как обычный Python-класс.

## 6. Добавление нового языка / Adding a New Language
- Установите нужную spaCy-модель (например, `python -m spacy download xx_ent_wiki_sm`).
- Укажите model_name в config для TripleExtractor и BoundarySegmenter.

## 7. Отладка и диагностика / Debugging
- Включите логирование (logging).
- Проверяйте промежуточные этапы пайплайна (см. pipeline.py).
- Используйте тесты из папки tests/.

## 8. Работа с большими файлами / Large Files
- Разбивайте текст на части, обрабатывайте батчами.
- Следите за памятью при использовании SBERT и HDBSCAN. 