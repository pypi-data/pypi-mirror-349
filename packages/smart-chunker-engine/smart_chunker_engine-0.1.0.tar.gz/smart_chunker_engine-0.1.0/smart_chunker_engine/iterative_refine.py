from typing import List, Dict, Any, Optional
import numpy as np
from smart_chunker_engine import metrics
from sentence_transformers import SentenceTransformer
import re

class IterativeRefiner:
    """Performs greedy MERGE/SPLIT operations on chunks based on scoring (см. 3.md)."""

    def __init__(self, lambda_: float = 0.4, theta_high: float = 0.75, theta_low: float = 0.35, epsilon: float = 1e-2, max_iter: int = 4,
                 model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2', device: Optional[str] = None):
        """Initialize IterativeRefiner with scoring parameters and SBERT model.

        Args:
            lambda_ (float): Weight for boundary penalty.
            theta_high (float): Merge threshold.
            theta_low (float): Split threshold.
            epsilon (float): Stop threshold for improvement.
            max_iter (int): Maximum number of iterations.
            model_name (str): SBERT model name.
            device (str, optional): 'cpu' or 'cuda'.
        """
        self.lambda_ = lambda_
        self.theta_high = theta_high
        self.theta_low = theta_low
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.model_name = model_name
        self.device = device or 'cpu'
        try:
            self.sbert = SentenceTransformer(model_name, device=self.device)
        except Exception:
            self.sbert = None
        self._emb_cache = {}

    def get_emb(self, chunk: Dict[str, Any]) -> np.ndarray:
        text = chunk['text']
        if text in self._emb_cache:
            return self._emb_cache[text]
        if self.sbert is not None:
            emb = self.sbert.encode(text, convert_to_numpy=True)
        else:
            emb = np.array([hash(text) % 1000], dtype=np.float32)
        self._emb_cache[text] = emb
        return emb

    def refine(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform iterative MERGE/SPLIT on chunks (см. 3.md).

        Применимость:
        - Если чанк слишком короткий (<20 символов) или содержит <2 предложений, split/merge не выполняется.
        - Для таких чанков метод возвращает их без изменений.

        Args:
            chunks (List[Dict[str, Any]]): List of chunk dicts (must have 'text').
        Returns:
            List[Dict[str, Any]]: Refined list of chunk dicts.
        """
        if not chunks or len(chunks) < 2:
            return list(chunks)
        # Если все чанки слишком короткие или <2 предложений — возвращаем как есть
        def _is_applicable(chunk):
            text = chunk['text']
            sents = re.split(r'[.!?]\s+', text.strip())
            sents = [s for s in sents if s]
            return len(text) >= 20 and len(sents) >= 2
        if not any(_is_applicable(c) for c in chunks):
            return list(chunks)
        chunks = list(chunks)
        self._emb_cache.clear()
        for _ in range(self.max_iter):
            improv = 0.0
            i = 0
            while i < len(chunks) - 1:
                # Пропускаем merge/split для коротких чанков
                if not _is_applicable(chunks[i]) or not _is_applicable(chunks[i+1]):
                    i += 1
                    continue
                emb_i = self.get_emb(chunks[i])
                emb_ip1 = self.get_emb(chunks[i+1])
                boundary_val = metrics.boundary(emb_i, emb_ip1)
                merged_text = chunks[i]['text'] + ' ' + chunks[i+1]['text']
                merged_emb = self.get_emb({'text': merged_text})
                gain_merge = self._gain_merge(chunks, i)
                if boundary_val > self.theta_high and gain_merge > 0:
                    chunks[i]['text'] = merged_text
                    del chunks[i+1]
                    improv += gain_merge
                    continue
                cohesion_val = self._cohesion_single(chunks[i])
                gain_split = self._gain_split(chunks, i)
                if cohesion_val < self.theta_low and gain_split > 0:
                    text = chunks[i]['text']
                    mid = len(text) // 2
                    left = {'text': text[:mid].strip()}
                    right = {'text': text[mid:].strip()}
                    chunks[i:i+1] = [left, right]
                    improv += gain_split
                    i -= 1
                i += 1
            if improv < self.epsilon:
                break
        return chunks

    def _cohesion_single(self, chunk: Dict[str, Any]) -> float:
        """Cohesion for a chunk: mean pairwise cosine similarity of sentence embeddings."""
        text = chunk['text']
        # Разбиваем на предложения (очень просто)
        sents = re.split(r'[.!?]\s+', text.strip())
        sents = [s for s in sents if s]
        if len(sents) < 2 or len(text) < 20:
            return 1.0
        embs = [self.get_emb({'text': s}) for s in sents]
        return metrics.cohesion(embs)

    def _gain_merge(self, chunks: List[Dict[str, Any]], i: int) -> float:
        # Не выполнять merge, если любой из чанков слишком короткий
        if len(chunks[i]['text']) < 20 or len(chunks[i+1]['text']) < 20:
            return 0.0
        before = self._score(chunks)
        merged = list(chunks)
        merged[i]['text'] = merged[i]['text'] + ' ' + merged[i+1]['text']
        del merged[i+1]
        after = self._score(merged)
        return after - before

    def _gain_split(self, chunks: List[Dict[str, Any]], i: int) -> float:
        text = chunks[i]['text']
        # Не split, если текст слишком короткий или <2 предложений
        sents = re.split(r'[.!?]\s+', text.strip())
        sents = [s for s in sents if s]
        if len(text) < 20 or len(sents) < 2:
            return 0.0
        before = self._score(chunks)
        mid = len(text) // 2
        left = {'text': text[:mid].strip()}
        right = {'text': text[mid:].strip()}
        splitted = list(chunks)
        splitted[i:i+1] = [left, right]
        after = self._score(splitted)
        return after - before

    def _score(self, chunks: List[Dict[str, Any]]) -> float:
        if len(chunks) < 2:
            return 0.0
        embs = [self.get_emb(c) for c in chunks]
        score = 0.0
        for i in range(len(chunks)-1):
            chunk_embs = [embs[i]]
            coh = metrics.cohesion(chunk_embs)
            bnd = metrics.boundary(embs[i], embs[i+1])
            score += coh - self.lambda_ * bnd
        return score 