# План реализации проекта "Smart Chunker Engine"

**Официальный репозиторий:** [git@github.com:maverikod/vvz-smart-chunker-engine.git](git@github.com:maverikod/vvz-smart-chunker-engine.git)

## Внешние зависимости и интеграция

- Для всех операций с метаданными чанков (создание, хранение, экспорт, валидация) используется внешний пакет **chunk_metadata_adapter** версии >=1.3.0.
- Все структуры данных `SemanticChunk`, `FlatSemanticChunk`, а также API для построения и конвертации метаданных берутся из этого пакета.
- Любые изменения в формате метаданных должны быть согласованы с документацией и тестами chunk_metadata_adapter.

## [_] Этап 1: Создание базовой структуры проекта и недостающих модулей

1. [_] **Создание структуры файлов для недостающих модулей**:
   - [_] `boundary.py` - модуль обнаружения границ
   - [_] `metablock.py` - модуль для работы с метаблоками
   - [_] `sentence_refine.py` - модуль для улучшения предложений внутри метаблоков
   - [_] `triple_extractor.py` - извлечение троек <N A V> с помощью spaCy
   - [_] `triple_cluster.py` - кластеризация троек с HDBSCAN и вычисление весов
   - [_] `iterative_refine.py` - алгоритм жадной оптимизации MERGE/SPLIT
   - [_] `metadata_builder.py` - создание метаданных для чанков (через chunk_metadata_adapter)
   - [_] `tfidf_layer.py` - обработка TF-IDF и весов слов
   - [_] `metrics.py` - расчет метрик качества чанков
   - [_] `lifecycle_validator.py` - валидация жизненного цикла чанков
   - [_] `exporter.py` - экспорт в FlatChunk (через chunk_metadata_adapter)

## [_] Этап 2: Разработка ключевых алгоритмических модулей

2. [_] **Модуль семантического окна (boundary_segmenter.py)**:
   - [_] Реализация POS-окна
   - [_] Интеграция SBERT для векторизации
   - [_] Определение границ на основе косинусного расстояния

3. [_] **Модуль статистического шлюза (stats_gate.py)**:
   - [_] Доработка расчета вариации, энтропии и коэффициента Джини
   - [_] Реализация логики принятия решения о включении TF-IDF слоя

4. [_] **Модуль извлечения троек и кластеризации**:
   - [_] `triple_extractor.py` - интеграция с spaCy для извлечения троек <N A V>
   - [_] `triple_cluster.py` - реализация кластеризации HDBSCAN и расчета весов

5. [_] **Модуль итеративного улучшения (iterative_refine.py)**:
   - [_] Реализация алгоритма MERGE/SPLIT с параметрами θ_high, θ_low, λ
   - [_] Функции для расчета метрик cohesion и boundary
   - [_] Логика остановки итераций при достижении порога прироста

## [_] Этап 3: Разработка вспомогательных модулей и интеграция

6. [_] **Модуль метаданных и жизненного цикла**:
   - [_] `metadata_builder.py` - создание и обогащение метаданных чанков (через chunk_metadata_adapter)
   - [_] `lifecycle_validator.py` - присвоение статусов RELIABLE/VALIDATED/REJECTED (использовать ChunkStatus из chunk_metadata_adapter)

7. [_] **Модуль экспорта и хранения**:
   - [_] `exporter.py` - преобразование в JSON и FlatSemanticChunk форматы (через chunk_metadata_adapter)
   - [_] Интеграция с векторной БД (опционально)

8. [_] **Улучшение основного пайплайна**:
   - [_] Обновление `pipeline.py` для включения всех модулей
   - [_] Реализация полного процесса обработки согласно схеме потока данных
   - [_] Все этапы, связанные с метаданными, используют API chunk_metadata_adapter

## [_] Этап 4: Тестирование и оценка качества

9. [_] **Разработка тестовых скриптов**:
   - [_] `evaluate_boundaries.py` - расчет F1 для границ чанков
   - [_] `calc_noise_rate.py` - определение процента шумовых чанков
   - [_] `length_stats.py` - анализ длины чанков и коэффициента вариации
   - [_] `coverage_check.py` - проверка покрытия темы в чанках
   - [_] `time_benchmark.py` и `memory_benchmark.py` - оценка производительности
   - [_] Тесты на корректность сериализации/десериализации через chunk_metadata_adapter

10. [_] **Создание тестовых корпусов**:
    - [_] Настройка директории `data/` для хранения тестовых корпусов
    - [_] Подготовка файлов `block_offsets.json` для корпусов
    - [_] Подготовка `gold_sentences.json` для проверки качества

## [_] Этап 5: CI/CD и документация

11. [_] **Настройка CI/CD**:
    - [_] Создание GitHub Actions workflow согласно ТЗ
    - [_] Настройка pytest с выводом в JUnit XML
    - [_] Добавление pre-commit хуков для smoke-тестов
    - [_] Проверка интеграции с chunk_metadata_adapter >=1.3.0

12. [_] **Документация и примеры**:
    - [_] Обновление README.md с описанием проекта
    - [_] Добавление документации по API (с примерами использования chunk_metadata_adapter)
    - [_] Создание примеров использования в директории examples/

## [_] Этап 6: Оптимизация и финализация

13. [_] **Оптимизация производительности**:
    - [_] Профилирование и оптимизация узких мест
    - [_] Параллелизация обработки, где возможно
    - [_] Кэширование и улучшение памяти

14. [_] **Финальное тестирование**:
    - [_] Проверка на всех тестовых корпусах
    - [_] Валидация соответствия KPI
    - [_] Исправление обнаруженных ошибок
    - [_] Проверка совместимости с chunk_metadata_adapter >=1.3.0

## [_] Приоритетный порядок разработки модулей:

1. boundary_segmenter.py
2. stats_gate.py
3. triple_extractor.py + triple_cluster.py
4. iterative_refine.py
5. metadata_builder.py (интеграция с chunk_metadata_adapter)
6. evaluate_boundaries.py

## Таблица зависимостей между модулями

| Модуль                | Зависит от                           | Используется в             |
|-----------------------|--------------------------------------|----------------------------|
| pre_normalize.py      | -                                    | pipeline.py                |
| token_pos.py          | pre_normalize.py                     | boundary_segmenter.py      |
| boundary_segmenter.py | token_pos.py, SBERT                  | pipeline.py                |
| stats_gate.py         | numpy                                | pipeline.py                |
| triple_extractor.py   | spaCy, token_pos.py                  | triple_cluster.py          |
| triple_cluster.py     | triple_extractor.py, HDBSCAN         | tfidf_layer.py             |
| tfidf_layer.py        | triple_cluster.py, numpy             | pipeline.py                |
| metablock.py          | boundary_segmenter.py                | pipeline.py                |
| iterative_refine.py   | metrics.py                           | pipeline.py                |
| metadata_builder.py   | iterative_refine.py, chunk_metadata_adapter | pipeline.py         |
| lifecycle_validator.py| metadata_builder.py, chunk_metadata_adapter | pipeline.py         |
| metrics.py            | numpy                                | iterative_refine.py        |
| exporter.py           | metadata_builder.py, chunk_metadata_adapter | pipeline.py         |

## Метрики завершенности этапов

| Этап | Критерий завершения | Ожидаемый срок (дней) |
|------|---------------------|------------------------|
| 1    | Созданы заглушки для всех модулей | 3 |
| 2    | Основные алгоритмы реализованы и проходят юнит-тесты | 7 |
| 3    | Полный пайплайн работает, генерирует JSON с использованием chunk_metadata_adapter | 5 |
| 4    | Тесты показывают F1 ≥ 0.85, Noise ≤ 5% | 4 |
| 5    | CI настроен, workflow проходит, интеграция с chunk_metadata_adapter проверена | 2 |
| 6    | Достигнуты все целевые KPI | 5 |

## Необходимые дополнительные зависимости

```
hdbscan>=0.8.29
scikit-learn>=1.0.0
spacy>=3.5.0
ru_core_news_md @ https://github.com/explosion/spacy-models/releases/download/ru_core_news_md-3.5.0/ru_core_news_md-3.5.0-py3-none-any.whl
chunk_metadata_adapter>=1.3.0
``` 