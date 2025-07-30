# Smart Chunker Engine: Общая картина / Pipeline Overview

## Назначение / Purpose
Smart Chunker Engine — это модульный пайплайн для интеллектуального разбиения текста на семантические чанки с богатыми метаданными. Используется для препроцессинга, анализа, построения датасетов, подготовки данных для ML/NLP.

## Архитектура / Architecture

```
raw_text ─▶ PreNormalizer ─▶ InitialSplitter ─▶ POS Filter ─▶ BoundarySegmenter
         └─▶ StatsGate ─▶ TripleExtractor ─▶ TripleCluster ─▶ TfidfLayer
         └─▶ MetablockSegmenter ─▶ SentenceRefine ─▶ IterativeRefiner
         └─▶ MetadataBuilder ─▶ Exporter
```

- Каждый этап — отдельный модуль, легко настраивается.
- Все метаданные и экспорт — только через chunk_metadata_adapter.
- Поддержка русского и английского (и других языков при наличии моделей).

## Поток данных / Data Flow
1. **PreNormalizer**: очистка и нормализация текста.
2. **InitialSplitter**: разбиение на базовые чанки.
3. **POS Filter**: фильтрация токенов по частям речи.
4. **BoundarySegmenter**: поиск границ по семантике (SBERT).
5. **StatsGate**: решение о необходимости TF-IDF.
6. **TripleExtractor/TripleCluster**: извлечение троек, кластеризация, веса.
7. **TfidfLayer**: расчет TF-IDF с учетом весов.
8. **MetablockSegmenter**: группировка чанков в метаблоки.
9. **SentenceRefine**: доработка на уровне предложений.
10. **IterativeRefiner**: жадная оптимизация чанков.
11. **MetadataBuilder**: сборка финальных метаданных.
12. **Exporter**: экспорт в нужный формат.

## Типовые сценарии / Typical Use Cases
- **ML/DS препроцессинг**: подготовка обучающих данных с метаданными.
- **Документирование**: автоматическое разбиение длинных текстов.
- **NLP пайплайны**: генерация чанков для downstream-задач.
- **CI/QA**: автоматическая валидация качества разбиения (F1, noise, CV).

## Интеграция / Integration
- Используйте класс `SmartChunkerPipeline`:
```python
from smart_chunker_engine.pipeline import SmartChunkerPipeline
pipeline = SmartChunkerPipeline(config)
chunks = pipeline.run(raw_text)
```
- Экспортируйте результат:
```python
from smart_chunker_engine.exporter import export_chunks
export_chunks(chunks, "output.json", format="json")
```
- Все параметры настраиваются через config (см. COMPONENTS.md).

## Ограничения / Limitations
- Для русского требуется spaCy модель `ru_core_news_md`.
- Для SBERT — sentence-transformers, для кластеризации — hdbscan.
- Для больших текстов — возможны ограничения по памяти (разбивайте на части).
- Для CSV/Parquet — экспорт только FlatSemanticChunk.

## Best Practices
- Используйте явный config для reproducibility.
- Проверяйте наличие всех моделей и зависимостей заранее.
- Для больших датасетов — обрабатывайте батчами.
- Для CI — используйте скрипты из `scripts/` для оценки качества. 