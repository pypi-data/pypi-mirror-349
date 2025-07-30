# Project Structure: Smart Chunker Engine

## Финальное эталонное дерево каталогов и файлов проекта

```text
.
├── README.md                  # Описание проекта, инструкция (RU/EN)
├── requirements.txt           # Зависимости Python
├── setup.py                   # Скрипт установки пакета
├── main.py                    # Точка входа (CLI или пример)
├── .gitignore                 # Исключения для git
├── config.yaml                # Основной конфиг пайплайна (пример)
├── PROJECT_STRUCTURE.md       # Описание структуры и стандартов (этот файл)
├── docs/                      # Документация, ТЗ, спецификации
│   ├── implementation_plan.md
│   ├── 0.md ... 7.md
│   └── ...
├── adapter_docs/              # Документация по chunk_metadata_adapter
│   └── ...
├── smart_chunker_engine/      # Исходный код (production)
│   ├── __init__.py
│   ├── pipeline.py
│   ├── pre_normalize.py
│   ├── token_pos.py
│   ├── boundary_segmenter.py
│   ├── stats_gate.py
│   ├── tfidf_layer.py
│   ├── triple_extractor.py
│   ├── triple_cluster.py
│   ├── metablock.py
│   ├── sentence_refine.py
│   ├── iterative_refine.py
│   ├── metrics.py
│   ├── metadata_builder.py
│   ├── lifecycle_validator.py
│   ├── exporter.py
│   └── utils/
│       └── ...
├── tests/                     # Модульные и интеграционные тесты
│   ├── test_pipeline.py
│   ├── test_boundary_segmenter.py
│   ├── test_stats_gate.py
│   ├── test_tfidf_layer.py
│   ├── test_triple_extractor.py
│   ├── test_triple_cluster.py
│   ├── test_iterative_refine.py
│   ├── test_metadata_builder.py
│   ├── test_metrics.py
│   ├── test_exporter.py
│   └── ...
├── examples/                  # Примеры использования
│   ├── simple_example.py
│   └── ...
├── scripts/                   # Вспомогательные скрипты
│   ├── data_downloader.py
│   └── ...
├── data/                      # Тестовые и демонстрационные данные
│   ├── input/
│   │   └── ...
│   └── output/
├── output/                    # Артефакты работы пайплайна (не versioned)
├── comparison_results/        # Результаты сравнения (не versioned)
├── __pycache__/               # Кэш Python (игнорируется)
├── .venv/                     # Виртуальное окружение (игнорируется)
├── .cursor/                   # Служебные файлы редактора (игнорируется)
└── .git/                      # Git-репозиторий (игнорируется)
```

---

**Примечания:**
- Все production-модули — только в `smart_chunker_engine/`.
- Тесты — только в `tests/`, структура повторяет основной пакет.
- Документация и спецификации — только в `docs/` и `adapter_docs/`.
- Примеры и утилиты — в `examples/` и `scripts/`.
- Данные для тестов и демонстраций — в `data/`.
- Временные, кэш- и служебные каталоги не versioned и игнорируются.

---

## Стандарт организации каталогов и файлов проекта

**1. Корневые каталоги (обязательные):**
- `smart_chunker_engine/` — основной пакет исходного кода (все production-модули, логика пайплайна, utils)
- `tests/` — модульные и интеграционные тесты (структура повторяет основной пакет)
- `docs/` — документация, спецификации, планы, ТЗ
- `examples/` — примеры использования, демонстрационные скрипты
- `scripts/` — вспомогательные и сервисные скрипты (загрузка данных, pre-commit, CI)
- `data/` — тестовые и демонстрационные датасеты, входные/выходные файлы для тестов
- `adapter_docs/` — документация и спецификации по chunk_metadata_adapter
- `output/`, `comparison_results/` — артефакты работы пайплайна, результаты сравнения (опционально, не versioned)

**2. Внутренняя структура исходного кода (`smart_chunker_engine/`):**
- Каждый модуль — отдельный файл (≤350 строк), имя в snake_case (например, `boundary_segmenter.py`)
- Вспомогательные функции — в подкаталоге `utils/`
- В каждом файле — только одна зона ответственности (SRP)
- Пакет должен содержать `__init__.py`

**3. Тесты (`tests/`):**
- Структура тестов повторяет структуру основного пакета
- Имена файлов: `test_<module>.py`
- Каждый публичный API покрывается тестом

**4. Документация (`docs/`):**
- Все ТЗ, планы, спецификации, схемы, примеры конфигов
- Имена файлов — по разделам или шагам (например, `implementation_plan.md`, `0.md`, ...)

**5. Примеры (`examples/`):**
- Минимальные и расширенные примеры использования API
- Имена файлов — по назначению (`simple_example.py`, `full_pipeline_example.py`)

**6. Скрипты (`scripts/`):**
- Вспомогательные утилиты, не входящие в основной пакет
- Имена — по действию (`data_downloader.py`, `pre_commit_check.py`)

**7. Данные (`data/`):**
- `input/` — исходные тексты, корпуса, примеры
- `output/` — результаты работы пайплайна на тестовых данных
- Внутри — только тестовые/демо-данные, не production

**8. Общие требования:**
- Только латиница, цифры, `_`, `-` в именах
- Без пробелов, кириллицы, спецсимволов
- Все каталоги и файлы — в `snake_case`, кроме корневых markdown-файлов (`README.md` и др.)
- Не versionить временные, кэш- и служебные каталоги (`__pycache__`, `.venv`, `.git`, `.cursor`, `output/`, `comparison_results/`)
- Каждый публичный API — с docstring (Google Style, EN)

---

**Note:**
- All metadata operations are performed via `chunk_metadata_adapter` (>=1.3.0) as per project standards.
- See `docs/implementation_plan.md` and `docs/metadata_adapter_patch_spec.md` for integration details.
- Source code modules (pipeline, segmentation, metrics, etc.) are to be implemented as per the implementation plan. 