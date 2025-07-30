# Technical Patch Specification: chunk_metadata_adapter for Chunker

## Purpose

This document provides an exact, actionable specification for the required changes to the `chunk_metadata_adapter` Python package to ensure full compatibility with the Chunker pipeline and its technical requirements.

---

## 1. Extend ChunkMetrics Model

**File:** `models.py`

Add the following optional fields to `ChunkMetrics`:

```python
class ChunkMetrics(BaseModel):
    # ... existing fields ...
    coverage: Optional[float] = Field(default=None, ge=0, le=1)
    cohesion: Optional[float] = Field(default=None, ge=0, le=1)        # NEW
    boundary_prev: Optional[float] = Field(default=None, ge=0, le=1)   # NEW
    boundary_next: Optional[float] = Field(default=None, ge=0, le=1)   # NEW
```

---

## 2. Extend FlatSemanticChunk Model

**File:** `models.py`

Add the same fields to `FlatSemanticChunk`:

```python
class FlatSemanticChunk(BaseModel):
    # ... existing fields ...
    coverage: Optional[float] = None
    cohesion: Optional[float] = None
    boundary_prev: Optional[float] = None
    boundary_next: Optional[float] = None
```

---

## 3. Update Converters

**File:** `models.py`

- В методе `FlatSemanticChunk.from_semantic_chunk()`:
    - Маппировать новые поля из `chunk.metrics` в flat-модель.
- В методе `FlatSemanticChunk.to_semantic_chunk()`:
    - Восстанавливать новые поля обратно в `ChunkMetrics`.

---

## 4. Update ChunkMetadataBuilder API

**File:** `metadata_builder.py`

- В методе `build_flat_metadata()`:
    - Добавить опциональные параметры: `coverage`, `cohesion`, `boundary_prev`, `boundary_next`.
    - Записывать их в возвращаемый dict.
- В методе `build_semantic_chunk()`:
    - Принимать либо объект `ChunkMetrics`, либо отдельные float-поля для новых метрик.
    - Корректно заполнять расширенный объект `ChunkMetrics`.

---

## 5. Status Case-Insensitivity

**File:** `models.py` (и/или валидаторы)

- Везде, где парсится статус (`ChunkStatus`), разрешить как lower-, так и upper-case строки:

```python
if isinstance(status, str):
    status = ChunkStatus(status.lower())
```

---

## 6. Backward Compatibility

- Все новые поля должны быть `Optional` и по умолчанию `None`.
- Старые JSON/CSV файлы должны оставаться валидными.
- Экспорт в CSV/Parquet должен добавлять новые колонки, но не ломать старые пайплайны.

---

## 7. Tests

- Добавить unit-тесты:
    - Проверка валидации новых полей (0 ≤ x ≤ 1).
    - Round-trip: `SemanticChunk` → `FlatSemanticChunk` → `SemanticChunk` с новыми метриками.
    - Проверка регистронезависимого парсинга статусов.

---

## 8. Documentation & Versioning

- Обновить документацию и примеры использования.
- Увеличить минорную версию (например, `1.2.1` → `1.3.0`).
- Добавить запись в `CHANGELOG.md`.

---

**End of specification** 