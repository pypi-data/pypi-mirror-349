# Smart Chunker Engine

Модульный фреймворк для интеллектуального разбиения текста на семантические чанки с богатыми метаданными (русский/английский).

---

## Возможности / Features
- Многоступенчатый пайплайн (нормализация, разбиение, семантика, метаданные)
- Гибкая настройка через config
- Поддержка русского и английского (и других языков при наличии моделей)
- Экспорт в JSON/CSV/Parquet (через chunk_metadata_adapter)
- Простая интеграция в ML/NLP пайплайны, API, CI

---

## Установка / Installation
```bash
pip install -r requirements.txt
# или
pip install .
```

---

## Быстрый старт / Quick Start
```python
from smart_chunker_engine.pipeline import SmartChunkerPipeline
pipeline = SmartChunkerPipeline()
chunks = pipeline.run("Это пример текста для разбиения на чанки.")
for c in chunks:
    print(c.text)
```

---

## Примеры использования / Usage Examples

### 1. Базовый пример (русский)
```python
from smart_chunker_engine.pipeline import SmartChunkerPipeline
pipeline = SmartChunkerPipeline()
text = "Это пример текста для разбиения на чанки. Каждый чанк будет содержать метаданные."
chunks = pipeline.run(text)
for c in chunks:
    print(f"[{c.start}:{c.end}] {c.text}")
```

### 2. Кастомные настройки пайплайна
```python
config = {
    'split': {'chunk_size': 50},
    'boundary': {'window_size': 10, 'threshold': 0.12},
    'stats_gate': {'var_thr': 0.1},
    'triple_cluster': {'min_cluster': 2},
    'tfidf': {'top_n': 100},
    'iter_refine': {'lambda_': 0.3, 'max_iter': 2}
}
pipeline = SmartChunkerPipeline(config)
chunks = pipeline.run("Текст для теста с кастомными параметрами.")
```

### 3. Экспорт чанков в JSON
```python
from smart_chunker_engine.exporter import export_chunks
export_chunks(chunks, "output.json", format="json")
```

### 4. Обработка английского текста
```python
config = {'split': {'chunk_size': 40}, 'spacy_model': 'en_core_web_sm'}
pipeline = SmartChunkerPipeline(config)
text = "This is an example of English text. The chunker works for multiple languages."
chunks = pipeline.run(text)
```

### 5. Обработка батча текстов
```python
pipeline = SmartChunkerPipeline({'split': {'chunk_size': 60}})
texts = ["Первый текст для чанкинга.", "Второй текст для примера."]
all_chunks = [pipeline.run(t) for t in texts]
```

### 6. Интеграция с pandas (DataFrame)
```python
import pandas as pd
from smart_chunker_engine.pipeline import SmartChunkerPipeline
pipeline = SmartChunkerPipeline()
df = pd.DataFrame({'text': ["Текст 1.", "Текст 2."]})
df['chunks'] = df['text'].apply(lambda t: pipeline.run(t))
```

---

## Описание основных настроек / Main Config Options

| Этап            | Ключ config         | Описание параметров                                   |
|-----------------|--------------------|-------------------------------------------------------|
| Split           | split              | chunk_size, overlap, language, chunk_type              |
| Boundary        | boundary           | window_size, step, threshold, model_name              |
| StatsGate       | stats_gate         | var_thr, ent_thr, gini_thr                            |
| TripleExtractor | spacy_model        | model_name (ru_core_news_md, en_core_web_sm, ...)     |
| TripleCluster   | triple_cluster     | min_cluster, model_name, device, batch_size           |
| TfidfLayer      | tfidf              | top_n                                                 |
| Metablock       | metablock          | threshold, model_name                                 |
| IterativeRefine | iter_refine        | lambda_, theta_high, theta_low, epsilon, max_iter, model_name, device |

**Пример полного config:**
```python
config = {
    'split': {'chunk_size': 100, 'overlap': 10, 'language': 'ru'},
    'boundary': {'window_size': 15, 'step': 5, 'threshold': 0.13},
    'stats_gate': {'var_thr': 0.12, 'ent_thr': 7.5, 'gini_thr': 0.2},
    'spacy_model': 'ru_core_news_md',
    'triple_cluster': {'min_cluster': 3, 'device': 'cpu'},
    'tfidf': {'top_n': 150},
    'metablock': {'threshold': 0.22},
    'iter_refine': {'lambda_': 0.35, 'theta_high': 0.7, 'theta_low': 0.3, 'epsilon': 0.005, 'max_iter': 3}
}
```

---

## Документация / Documentation
- [COMPONENTS.md](docs/COMPONENTS.md) — описание всех модулей
- [PIPELINE_OVERVIEW.md](docs/PIPELINE_OVERVIEW.md) — архитектура и поток данных
- [FAQ.md](docs/FAQ.md), [HOWTO.md](docs/HOWTO.md) — практические советы
- Примеры: [examples/](examples/)
- Тесты: [tests/](tests/)

---

## License
MIT 