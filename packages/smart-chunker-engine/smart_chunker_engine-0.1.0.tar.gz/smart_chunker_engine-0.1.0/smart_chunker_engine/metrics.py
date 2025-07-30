import numpy as np
from scipy.spatial.distance import cosine
from typing import List, Optional


def cohesion(embeddings: List[np.ndarray]) -> float:
    """Compute mean pairwise cosine similarity (cohesion) for a list of embeddings.

    Args:
        embeddings (List[np.ndarray]): List of chunk embeddings.
    Returns:
        float: Mean pairwise cosine similarity (0..1), or 0 if <2 embeddings.
    """
    n = len(embeddings)
    if n < 2:
        return 0.0
    sims = []
    for i in range(n):
        for j in range(i+1, n):
            sim = 1 - cosine(embeddings[i], embeddings[j])
            sims.append(sim)
    return float(np.mean(sims)) if sims else 0.0


def boundary(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings (boundary metric).

    Args:
        emb1 (np.ndarray): Embedding of last element in chunk i.
        emb2 (np.ndarray): Embedding of first element in chunk i+1.
    Returns:
        float: Cosine similarity (0..1).
    """
    return float(1 - cosine(emb1, emb2))


def coverage(sentence_emb: np.ndarray, topic_core_emb: np.ndarray) -> float:
    """Compute coverage metric: 1 - cosine(sentence_emb, topic_core_emb).

    Args:
        sentence_emb (np.ndarray): Embedding of the sentence or chunk.
        topic_core_emb (np.ndarray): Embedding of the topic core.
    Returns:
        float: Coverage metric (0..1).
    """
    return float(1 - cosine(sentence_emb, topic_core_emb))


def off_topic(coverage_value: float, threshold: float = 0.6) -> bool:
    """Determine if a chunk is off-topic based on coverage.

    Args:
        coverage_value (float): Coverage metric (0..1).
        threshold (float): Threshold for off-topic tag.
    Returns:
        bool: True if off-topic, False otherwise.
    """
    return coverage_value < threshold


def boundary_metrics(
    chunk_embeddings: List[np.ndarray],
) -> List[dict]:
    """Compute boundary_prev and boundary_next for each chunk.

    Args:
        chunk_embeddings (List[np.ndarray]): List of chunk embeddings.
    Returns:
        List[dict]: List of dicts with 'boundary_prev', 'boundary_next' for each chunk.
    """
    n = len(chunk_embeddings)
    result = []
    for i in range(n):
        prev = boundary(chunk_embeddings[i-1], chunk_embeddings[i]) if i > 0 else None
        next_ = boundary(chunk_embeddings[i], chunk_embeddings[i+1]) if i < n-1 else None
        result.append({'boundary_prev': prev, 'boundary_next': next_})
    return result 