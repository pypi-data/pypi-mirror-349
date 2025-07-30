"""
token_pos.py

POS filter for tokens: keeps only Nouns, Verbs, Adjectives.
Uses spaCy if available, else falls back to simple split.

Public API:
    filter_pos_tokens(text: str) -> list[str]
"""
from typing import List

try:
    import spacy
    _nlp = spacy.load('en_core_web_sm')
except ImportError:
    _nlp = None

_POS_TAGS = {"NOUN", "VERB", "ADJ"}

def filter_pos_tokens(text: str) -> List[str]:
    """Filter tokens by POS (NOUN, VERB, ADJ).

    Args:
        text (str): Input text.
    Returns:
        List[str]: Filtered tokens.
    """
    if _nlp:
        doc = _nlp(text)
        return [token.text for token in doc if token.pos_ in _POS_TAGS]
    # Fallback: naive split
    return text.split() 