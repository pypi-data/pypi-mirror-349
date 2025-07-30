# CHANGE REQUEST: Metadata Adapter Extension for **Chunker** Project

| Item | Value |
|------|-------|
| **Request ID** | CR-2025-Chunker-MA-001 |
| **Requested by** | Chunker Core Team |
| **Date** | 2025-05-20 |
| **Affected Component** | `chunk_metadata_adapter` (Python package) |
| **Priority** | High (release blocker) |
| **Target Version** | `chunk_metadata_adapter` ≥ 0.5.0 |

---

## 1. Background

The **Chunker** pipeline relies on rich metadata (`SemanticChunk` / `FlatSemanticChunk`) that include advanced quality metrics (cohesion, boundary similarity, etc.).

The current public package `chunk_metadata_adapter` (version distributed via PyPI) does not expose several mandatory fields and API hooks specified in the Chunker Technical Specification (docs `0.md`–`4.md`).

This change request formalises the **gap-analysis** and lists the **mandatory modifications** that must be delivered to ensure seamless integration.

---

## 2. Problem Statement

1. `ChunkMetrics` model misses three metric fields required by the spec.
2. `FlatSemanticChunk` lacks matching columns ⇒ export breaks.
3. `ChunkMetadataBuilder` API cannot populate the new metrics.
4. `ChunkStatus` string values are case-sensitive and conflict with upper-case constants used in the pipeline.

Without these changes the Chunker CI fails at the metadata validation stage (Part 4 §4.5 JSON-Schema).

---

## 3. Scope of Work

### 3.1 Data Model Updates (`models.py`)

```python
class ChunkMetrics(BaseModel):
    # existing fields …
    coverage: Optional[float] = Field(None, ge=0, le=1)
    cohesion: Optional[float] = Field(None, ge=0, le=1)          # NEW
    boundary_prev: Optional[float] = Field(None, ge=0, le=1)     # NEW
    boundary_next: Optional[float] = Field(None, ge=0, le=1)     # NEW
```

Extend `FlatSemanticChunk` with **optional** float fields:
`coverage`, `cohesion`, `boundary_prev`, `boundary_next` (range 0-1).

### 3.2 Converters

* `FlatSemanticChunk.from_semantic_chunk()` — map the four new metrics → flat model.
* `FlatSemanticChunk.to_semantic_chunk()` — reconstruct metrics from flat → structured.

### 3.3 Builder API (`metadata_builder.py`)

* `build_flat_metadata()` — accept the four floats (optional) and write them.
* `build_semantic_chunk()` — accept a pre-built `ChunkMetrics` or the same four floats; create/populate extended `ChunkMetrics`.

### 3.4 Status Handling

Make parsing of `ChunkStatus` **case-insensitive**:

```python
if isinstance(status, str):
    status = ChunkStatus(status.lower())
```

### 3.5 Version Bump & Changelog

* Increment minor version → `0.X + 1` (semantic versioning).
* Add entry in `CHANGELOG.md` under **Added** and **Changed**.

---

## 4. Impact & Compatibility

* **Backward-compatible:** new fields are optional; existing clients remain valid.
* CSV/Parquet exporters need to append columns — verified by Chunker tests.
* No breaking changes to existing public methods.

---

## 5. Acceptance Criteria

1. New fields visible in both models; Pydantic validation passes.
2. Round-trip conversion keeps metric values with tolerance `1e-6`.
3. Case-insensitive status strings (`"RAW"`, `"raw"`) accepted.
4. All unit-tests (existing + new) green under Python 3.10–3.12.
5. Package published to TestPyPI (`0.5.0rc1`) for integration testing.
6. Updated documentation & changelog.

---

## 6. Proposed Timeline

| Milestone | Date |
|-----------|------|
| Dev branch ready | **2025-05-27** |
| RC on TestPyPI | 2025-05-29 |
| Final release | 2025-05-30 |

---

## 7. Contacts

* **Chunker Tech Lead:** <techlead@chunker.dev>
* **Metadata Adapter Maintainer:** <maintainer@adapter.dev>

---

*End of Change Request* 