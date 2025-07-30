"""
sentence_refine.py

Sentence refinement inside metablock: merges short sentences, splits long ones.

Public API:
    refine_sentences(metablock: list[str]) -> list[str]
"""
from typing import List

MIN_LEN = 20
MAX_LEN = 120

def refine_sentences(metablock: List[str]) -> List[str]:
    """Refine sentences inside a metablock: merge short, split long.

    Args:
        metablock (List[str]): List of sentences in metablock.
    Returns:
        List[str]: Refined sentences.
    """
    refined = []
    buffer = ""
    for sent in metablock:
        if len(sent) < MIN_LEN:
            buffer += (" " if buffer else "") + sent
            if len(buffer) >= MIN_LEN:
                refined.append(buffer.strip())
                buffer = ""
        elif len(sent) > MAX_LEN:
            # Improved split: accumulate parts until MIN_LEN, then flush
            parts = [s.strip() for s in sent.split('.') if s.strip()]
            buf = ""
            for p in parts:
                if buf:
                    buf += ". " + p
                else:
                    buf = p
                if len(buf) >= MIN_LEN:
                    refined.append(buf.strip())
                    buf = ""
            if buf:
                refined.append(buf.strip())
        else:
            if buffer:
                refined.append(buffer.strip())
                buffer = ""
            refined.append(sent)
    if buffer:
        refined.append(buffer.strip())
    return refined 