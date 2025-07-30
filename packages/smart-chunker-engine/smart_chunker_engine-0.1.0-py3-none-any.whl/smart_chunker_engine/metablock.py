from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

class MetablockSegmenter:
    """Splits chunks into metablocks using semantic axes (N/A/V vectors)."""

    def __init__(self, threshold: float = 0.25, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """Initialize MetablockSegmenter with axis threshold and SBERT model.

        Args:
            threshold (float): Threshold for axis difference.
            model_name (str): SBERT model name.
        """
        self.threshold = threshold
        self.model = SentenceTransformer(model_name)

    def split(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Split chunks into metablocks based on semantic axes.

        Args:
            chunks (List[Dict[str, Any]]): List of chunk dicts (must have 'text').
        Returns:
            List[Dict[str, Any]]: List of metablock dicts.
        """
        if not chunks or len(chunks) < 2:
            return list(chunks)
        # For demo: use SBERT embedding of each chunk text as axis
        embeddings = [self.model.encode(chunk['text'], convert_to_numpy=True) for chunk in chunks]
        metablocks = []
        current_block = [chunks[0]]
        for i in range(1, len(chunks)):
            delta = cosine(embeddings[i-1], embeddings[i])
            if delta > self.threshold:
                metablocks.append({'chunks': current_block})
                current_block = [chunks[i]]
            else:
                current_block.append(chunks[i])
        if current_block:
            metablocks.append({'chunks': current_block})
        return metablocks 