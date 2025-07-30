import json
import csv
from typing import List, Union, Any, Dict, Optional
from pathlib import Path
from chunk_metadata_adapter import SemanticChunk, FlatSemanticChunk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def export_semantic_chunks_json(
    chunks: List[SemanticChunk],
    path: Union[str, Path],
    indent: int = 2
) -> None:
    """Export a list of SemanticChunk objects to a JSON file.

    Args:
        chunks: List of SemanticChunk objects.
        path: Output file path.
        indent: Indentation for JSON (default: 2).
    """
    data = [chunk.model_dump() for chunk in chunks]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def export_flat_chunks_csv(
    chunks: List[FlatSemanticChunk],
    path: Union[str, Path],
    delimiter: str = ","
) -> None:
    """Export a list of FlatSemanticChunk objects to a CSV file.

    Args:
        chunks: List of FlatSemanticChunk objects.
        path: Output file path.
        delimiter: CSV delimiter (default: ',').
    """
    if not chunks:
        raise ValueError("No chunks to export.")
    fieldnames = list(chunks[0].model_dump().keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        for chunk in chunks:
            writer.writerow(chunk.model_dump())


def export_flat_chunks_parquet(
    chunks: List[FlatSemanticChunk],
    path: Union[str, Path]
) -> None:
    """Export a list of FlatSemanticChunk objects to a Parquet file (if pandas is available).

    Args:
        chunks: List of FlatSemanticChunk objects.
        path: Output file path.
    Raises:
        ImportError: If pandas is not installed.
    """
    if not HAS_PANDAS:
        raise ImportError("pandas is required for Parquet export.")
    if not chunks:
        raise ValueError("No chunks to export.")
    df = pd.DataFrame([chunk.model_dump() for chunk in chunks])
    df.to_parquet(path, index=False)


def export_chunks(
    chunks: List[Union[SemanticChunk, FlatSemanticChunk]],
    path: Union[str, Path],
    format: str = "json"
) -> None:
    """Universal export function for chunk metadata.

    Args:
        chunks: List of SemanticChunk or FlatSemanticChunk objects.
        path: Output file path.
        format: 'json', 'csv', or 'parquet'.
    """
    if not chunks:
        raise ValueError("No chunks to export.")
    if format == "json":
        if isinstance(chunks[0], SemanticChunk):
            export_semantic_chunks_json(chunks, path)
        elif isinstance(chunks[0], FlatSemanticChunk):
            # FlatSemanticChunk as JSON
            data = [chunk.model_dump() for chunk in chunks]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise TypeError("Unknown chunk type for JSON export.")
    elif format == "csv":
        if not isinstance(chunks[0], FlatSemanticChunk):
            raise TypeError("CSV export only supported for FlatSemanticChunk.")
        export_flat_chunks_csv(chunks, path)
    elif format == "parquet":
        if not isinstance(chunks[0], FlatSemanticChunk):
            raise TypeError("Parquet export only supported for FlatSemanticChunk.")
        export_flat_chunks_parquet(chunks, path)
    else:
        raise ValueError(f"Unknown export format: {format}") 