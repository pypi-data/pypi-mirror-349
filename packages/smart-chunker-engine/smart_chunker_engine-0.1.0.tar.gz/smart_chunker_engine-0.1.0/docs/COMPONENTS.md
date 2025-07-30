# Smart Chunker Engine: Документация по компонентам / Component Reference

## Оглавление / Table of Contents
- [Общая архитектура](#общая-архитектура)
- [PreNormalizer](#prenormalizer)
- [InitialSplitter](#initialsplitter)
- [POS Token Filter](#pos-token-filter)
- [BoundarySegmenter](#boundarysegmenter)
- [StatsGate](#statsgate)
- [TripleExtractor](#tripleextractor)
- [TripleCluster](#triplecluster)
- [TfidfLayer](#tfidflayer)
- [MetablockSegmenter](#metablocksegmenter)
- [SentenceRefine](#sentencerefine)
- [IterativeRefiner](#iterativerefiner)
- [MetadataBuilder](#metadatabuilder)
- [Exporter](#exporter)

---

## Общая архитектура / General Architecture

Пайплайн Smart Chunker Engine реализует многоступенчатую обработку текста для выделения семантических чанков с богатыми метаданными. Каждый этап отвечает за отдельную задачу и может быть гибко настроен через конфиг.

**Основные этапы:**
1. PreNormalizer — нормализация текста
2. InitialSplitter — первичное разбиение
3. POS Token Filter — фильтрация по частям речи
4. BoundarySegmenter — поиск границ по семантике
5. StatsGate — статистический шлюз (решение о TF-IDF)
6. TripleExtractor — извлечение троек (N, A, V)
7. TripleCluster — кластеризация троек, веса
8. TfidfLayer — расчет TF-IDF с учетом весов
9. MetablockSegmenter — группировка в метаблоки
10. SentenceRefine — доработка на уровне предложений
11. IterativeRefiner — жадная оптимизация чанков
12. MetadataBuilder — сборка метаданных
13. Exporter — экспорт в нужный формат

---

## PreNormalizer
**Назначение:**
- Unicode NFC-нормализация
- Удаление управляющих символов
- Очистка пробелов, табуляций, переводов строк

**Параметры:**
| Параметр | Тип | Описание | Default |
|----------|-----|----------|---------|
| config   | dict| Опции нормализации (обычно не требуется) | None |

**Использование:**
```python
from smart_chunker_engine.pre_normalize import PreNormalizer
norm = PreNormalizer()
clean_text = norm.normalize(raw_text)
```

**Нюансы:**
- Не требует внешних зависимостей.
- Работает одинаково для всех языков.

---

## InitialSplitter
**Назначение:**
- Делит нормализованный текст на чанки фиксированной или гибридной длины.
- Генерирует объекты SemanticChunk (без метрик).

**Параметры:**
| Параметр    | Тип   | Описание | Default |
|-------------|-------|----------|---------|
| chunk_size  | int   | Размер чанка (символы) | 500 |
| overlap     | int   | Перекрытие чанков (символы) | 0 |
| language    | str   | Язык чанка | 'ru' |
| chunk_type  | Enum  | Тип чанка (DocBlock и др.) | DocBlock |
| config      | dict  | Конфиг (переопределяет параметры) | None |

**Использование:**
```python
from smart_chunker_engine.initial_split import InitialSplitter
splitter = InitialSplitter(chunk_size=300)
chunks = splitter.split(text)
```

**Нюансы:**
- Если текст короче chunk_size — возвращает 1 чанк.
- Для overlap > 0 чанки могут пересекаться.

---

## POS Token Filter
**Назначение:**
- Оставляет только токены с POS: NOUN, VERB, ADJ.
- Использует spaCy, fallback — split по пробелу.

**Параметры:**
| Параметр | Тип | Описание | Default |
|----------|-----|----------|---------|
| text     | str | Входной текст | — |

**Использование:**
```python
from smart_chunker_engine.token_pos import filter_pos_tokens
tokens = filter_pos_tokens(text)
```

**Нюансы:**
- Для русского — требуется spaCy модель ru_core_news_md.
- Если spaCy не установлен — просто split.

---

## BoundarySegmenter
**Назначение:**
- Находит семантические границы между окнами токенов с помощью SBERT.

**Параметры:**
| Параметр    | Тип   | Описание | Default |
|-------------|-------|----------|---------|
| window_size | int   | Размер окна | 20 |
| step        | int   | Шаг окна | 10 |
| threshold   | float | Порог косинусного расстояния | 0.15 |
| model_name  | str   | SBERT-модель | paraphrase-multilingual-MiniLM-L12-v2 |

**Использование:**
```python
from smart_chunker_engine.boundary_segmenter import BoundarySegmenter
bs = BoundarySegmenter(window_size=15)
boundaries = bs.segment(tokens)
```

**Нюансы:**
- Требует sentence-transformers.
- Для малых текстов (<2 окна) возвращает пустой список.

---

## StatsGate
**Назначение:**
- Решает, включать ли TF-IDF слой, по статистикам токенов (дисперсия, энтропия, Джини).

**Параметры:**
| Параметр | Тип   | Описание | Default |
|----------|-------|----------|---------|
| var_thr  | float | Порог дисперсии | 0.15 |
| ent_thr  | float | Порог энтропии | 8.0 |
| gini_thr | float | Порог Джини | 0.25 |

**Использование:**
```python
from smart_chunker_engine.stats_gate import StatsGate
gate = StatsGate(var_thr=0.1)
use_tfidf = gate.should_enable(tokens)
```

**Нюансы:**
- Включает TF-IDF, если >=2 метрики превышают порог.

---

## TripleExtractor
**Назначение:**
- Извлекает тройки (NOUN, ADJ, VERB) из текста с помощью spaCy.

**Параметры:**
| Параметр   | Тип   | Описание | Default |
|------------|-------|----------|---------|
| model_name | str   | spaCy-модель | ru_core_news_md |

**Использование:**
```python
from smart_chunker_engine.triple_extractor import TripleExtractor
te = TripleExtractor()
triples = te.extract(text)
```

**Нюансы:**
- Для русского — требуется spaCy ru_core_news_md.
- Для коротких предложений троек может быть мало.

---

## TripleCluster
**Назначение:**
- Кластеризует тройки с помощью HDBSCAN, вычисляет веса токенов.

**Параметры:**
| Параметр      | Тип   | Описание | Default |
|---------------|-------|----------|---------|
| min_cluster   | int   | Мин. размер кластера | 5 |
| model_name    | str   | SBERT-модель | paraphrase-multilingual-MiniLM-L12-v2 |
| device        | str   | 'cpu'/'cuda' | None |
| batch_size    | int   | Размер батча | 1000 |

**Использование:**
```python
from smart_chunker_engine.triple_cluster import TripleCluster
tc = TripleCluster(min_cluster=3)
weights = tc.cluster(triples)
```

**Нюансы:**
- Если троек меньше min_cluster — веса по умолчанию (1.0).
- Требует sentence-transformers и hdbscan.

---

## TfidfLayer
**Назначение:**
- Считает TF-IDF для токенов с учетом весов.

**Параметры:**
| Параметр | Тип   | Описание | Default |
|----------|-------|----------|---------|
| top_n    | int   | Сколько лемм учитывать | 1000 |

**Использование:**
```python
from smart_chunker_engine.tfidf_layer import TfidfLayer
tfidf = TfidfLayer(top_n=100)
scores = tfidf.compute(tokens, weights)
```

**Нюансы:**
- Требует scikit-learn.
- Если токенов мало — возвращает пустой dict.

---

## MetablockSegmenter
**Назначение:**
- Группирует чанки в метаблоки по семантической близости (SBERT).

**Параметры:**
| Параметр   | Тип   | Описание | Default |
|------------|-------|----------|---------|
| threshold  | float | Порог различия осей | 0.25 |
| model_name | str   | SBERT-модель | paraphrase-multilingual-MiniLM-L12-v2 |

**Использование:**
```python
from smart_chunker_engine.metablock import MetablockSegmenter
mb = MetablockSegmenter(threshold=0.2)
blocks = mb.split(list_of_chunks)
```

**Нюансы:**
- Для малых текстов возвращает исходные чанки.

---

## SentenceRefine
**Назначение:**
- Объединяет короткие предложения, делит длинные внутри метаблока.

**Параметры:**
| Параметр | Тип | Описание | Default |
|----------|-----|----------|---------|
| metablock| list| Список предложений | — |

**Использование:**
```python
from smart_chunker_engine.sentence_refine import refine_sentences
refined = refine_sentences(sent_list)
```

**Нюансы:**
- MIN_LEN=20, MAX_LEN=120 (жестко заданы).

---

## IterativeRefiner
**Назначение:**
- Жадная оптимизация чанков: MERGE/SPLIT по метрикам.

**Параметры:**
| Параметр   | Тип   | Описание | Default |
|------------|-------|----------|---------|
| lambda_    | float | Вес штрафа за границу | 0.4 |
| theta_high | float | Порог для merge | 0.75 |
| theta_low  | float | Порог для split | 0.35 |
| epsilon    | float | Порог остановки | 0.01 |
| max_iter   | int   | Макс. итераций | 4 |
| model_name | str   | SBERT-модель | paraphrase-multilingual-MiniLM-L12-v2 |
| device     | str   | 'cpu'/'cuda' | None |

**Использование:**
```python
from smart_chunker_engine.iterative_refine import IterativeRefiner
refiner = IterativeRefiner(lambda_=0.3)
refined = refiner.refine(list_of_chunks)
```

**Нюансы:**
- Для коротких чанков (<20 символов, <2 предложений) skip MERGE/SPLIT.

---

## MetadataBuilder
**Назначение:**
- Собирает объекты SemanticChunk и FlatSemanticChunk с метриками.

**Параметры:**
| Параметр | Тип | Описание | Default |
|----------|-----|----------|---------|
| Все поля SemanticChunk/FlatSemanticChunk | — | — | — |

**Использование:**
```python
from smart_chunker_engine.metadata_builder import MetadataBuilder
mb = MetadataBuilder()
chunk = mb.build_semantic_chunk(text, start, end, method="pipeline")
```

**Нюансы:**
- Все метаданные строго через chunk_metadata_adapter.

---

## Exporter
**Назначение:**
- Экспортирует чанки в JSON, CSV, Parquet (SemanticChunk/FlatSemanticChunk).

**Параметры:**
| Параметр | Тип | Описание | Default |
|----------|-----|----------|---------|
| chunks   | list| Список чанков | — |
| path     | str | Путь к файлу | — |
| format   | str | Формат ('json', 'csv', 'parquet') | 'json' |

**Использование:**
```python
from smart_chunker_engine.exporter import export_chunks
export_chunks(chunks, "out.json", format="json")
```

**Нюансы:**
- Для Parquet требуется pandas.
- Для CSV — только FlatSemanticChunk. 