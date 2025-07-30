from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

class BoundarySegmenter:
    """Detects semantic boundaries in tokenized text using SBERT and windowing."""

    def __init__(self, window_size: int = 20, step: int = 10, threshold: float = 0.15, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """Initialize BoundarySegmenter with window size, step, threshold, and SBERT model name.

        Args:
            window_size (int): Size of the sliding window.
            step (int): Step size for the window.
            threshold (float): Cosine distance threshold for boundary detection.
            model_name (str): SBERT model name.
        """
        self.window_size = window_size
        self.step = step
        self.threshold = threshold
        self.model = SentenceTransformer(model_name)

    def segment(self, tokens: List[str]) -> List[int]:
        """Detect boundaries in tokenized text using SBERT window embeddings.

        Args:
            tokens (List[str]): List of tokens after POS filtering.
        Returns:
            List[int]: Indices of detected boundaries.
        """
        if not tokens or len(tokens) < self.window_size * 2:
            return []
        windows = []
        indices = []
        for i in range(0, len(tokens) - self.window_size + 1, self.step):
            window = tokens[i:i + self.window_size]
            windows.append(' '.join(window))
            indices.append(i)
        embeddings = self.model.encode(windows, convert_to_numpy=True)
        boundaries = []
        for i in range(len(embeddings) - 1):
            dist = cosine(embeddings[i], embeddings[i + 1])
            if dist > self.threshold:
                # boundary index is at the end of the first window
                boundary_idx = indices[i] + self.window_size - 1
                boundaries.append(boundary_idx)
        # Remove duplicates and sort
        return sorted(set(boundaries)) 