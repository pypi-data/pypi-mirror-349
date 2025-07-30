"""
window_segment.py

Window-based segmentation of token sequences.

Public API:
    window_segment(tokens: list[str], window_size: int, step_size: int) -> list[tuple[int, int]]
"""
from typing import List, Tuple

def window_segment(tokens: List[str], window_size: int, step_size: int) -> List[Tuple[int, int]]:
    """Segment tokens into windows.

    Args:
        tokens (List[str]): List of tokens.
        window_size (int): Size of each window.
        step_size (int): Step between windows.
    Returns:
        List[Tuple[int, int]]: List of (start, end) indices for each window.
    """
    n = len(tokens)
    windows = []
    for start in range(0, n, step_size):
        end = min(start + window_size, n)
        if end - start > 0:
            windows.append((start, end))
        if end == n:
            break
    return windows 