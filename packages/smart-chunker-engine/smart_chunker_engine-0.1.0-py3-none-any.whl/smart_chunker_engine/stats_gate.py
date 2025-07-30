from typing import List
import numpy as np
from collections import Counter

class StatsGate:
    """Decides whether to enable TF-IDF layer based on statistical metrics."""

    def __init__(self, var_thr: float = 0.15, ent_thr: float = 8.0, gini_thr: float = 0.25):
        """Initialize StatsGate with thresholds for variance, entropy, and Gini.

        Args:
            var_thr (float): Variance threshold.
            ent_thr (float): Entropy threshold.
            gini_thr (float): Gini coefficient threshold.
        """
        self.var_thr = var_thr
        self.ent_thr = ent_thr
        self.gini_thr = gini_thr

    def should_enable(self, tokens: List[str]) -> bool:
        """Determine if TF-IDF layer should be enabled based on statistics.

        Args:
            tokens (List[str]): List of tokens.
        Returns:
            bool: True if TF-IDF should be enabled, False otherwise.
        """
        if not tokens:
            return False
        counts = np.array(list(Counter(tokens).values()))
        probs = counts / counts.sum()
        # Variance of token frequencies (normalized)
        var_tf = np.var(probs)
        # Entropy (bits)
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        # Gini coefficient
        gini = 1 - np.sum(probs ** 2)
        # >=2 metrics must pass threshold
        passed = sum([
            var_tf > self.var_thr,
            entropy > self.ent_thr,
            gini > self.gini_thr
        ])
        return passed >= 2 