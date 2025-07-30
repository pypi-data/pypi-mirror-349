from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TfidfLayer:
    """Calculates TF-IDF and word weights for tokens."""

    def __init__(self, top_n: int = 1000):
        """Initialize TfidfLayer with number of top lemmas.

        Args:
            top_n (int): Number of top lemmas to keep.
        """
        self.top_n = top_n
        self.vectorizer = TfidfVectorizer(analyzer='word', lowercase=False, max_features=top_n)

    def compute(self, tokens: List[str], weights: Dict[str, float]) -> Dict[str, float]:
        """Compute TF-IDF scores and apply token weights.

        Args:
            tokens (List[str]): List of tokens.
            weights (Dict[str, float]): Token weights from triple clustering.
        Returns:
            Dict[str, float]: Mapping from token to weighted TF-IDF score.
        """
        if not tokens:
            return {}
        doc = ' '.join(tokens)
        tfidf_matrix = self.vectorizer.fit_transform([doc])
        feature_names = self.vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        result = {}
        for token, score in zip(feature_names, tfidf_scores):
            weight = weights.get(token, 1.0)
            result[token] = float(score) * float(weight)
        return result 