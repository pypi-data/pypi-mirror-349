from typing import List, Tuple, Dict, Optional
import numpy as np
import hdbscan
from sentence_transformers import SentenceTransformer
from collections import Counter, defaultdict
import math

class TripleCluster:
    """Clusters triples and computes token weights using HDBSCAN. Supports batching and device selection."""

    def __init__(self, min_cluster: int = 5, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2', device: Optional[str] = None, batch_size: int = 1000):
        """Initialize TripleCluster with minimum cluster size, SBERT model, device, and batch size.

        Args:
            min_cluster (int): Minimum cluster size for HDBSCAN.
            model_name (str): SBERT model name for triple embedding.
            device (str, optional): 'cpu' or 'cuda'. If None, auto.
            batch_size (int): Max triples to process in one batch.
        """
        self.min_cluster = min_cluster
        self.model = SentenceTransformer(model_name, device=device or 'cpu')
        self.batch_size = batch_size

    def cluster(self, triples: List[Tuple[str, str, str]]) -> Dict[str, float]:
        """Cluster triples and compute token weights. Processes in batches if needed.

        Args:
            triples (List[Tuple[str, str, str]]): List of triples.
        Returns:
            Dict[str, float]: Mapping from token to weight.
        """
        if not triples:
            return {}
        if len(triples) < self.min_cluster:
            # Not enough triples for clustering, assign default weight 1.0
            token_weights = defaultdict(float)
            for triple in triples:
                for token in triple:
                    token_weights[token] = max(token_weights[token], 1.0)
            return dict(token_weights)
        token_weights = defaultdict(float)
        n = len(triples)
        for start in range(0, n, self.batch_size):
            batch = triples[start:start+self.batch_size]
            triple_texts = [" ".join(t) for t in batch]
            embeddings = self.model.encode(triple_texts, convert_to_numpy=True)
            clusterer = hdbscan.HDBSCAN(min_cluster_size=self.min_cluster)
            labels = clusterer.fit_predict(embeddings)
            cluster_sizes = Counter(labels)
            for triple, label in zip(batch, labels):
                size = cluster_sizes[label] if label != -1 else 1
                for token in triple:
                    # weight = 1 + ln(1+size(cluster)), take max if token in several batches
                    token_weights[token] = max(token_weights[token], 1.0 + math.log(1 + size))
        return dict(token_weights) 