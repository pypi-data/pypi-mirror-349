from typing import List, Tuple
import spacy

class TripleExtractor:
    """Extracts triples <N A V> from text using spaCy."""

    def __init__(self, model_name: str = "ru_core_news_md"):
        """Initialize TripleExtractor with spaCy model.

        Args:
            model_name (str): spaCy model name.
        """
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def extract(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract triples from text.

        Args:
            text (str): Input text.
        Returns:
            List[Tuple[str, str, str]]: List of (N, A, V) triples.
        """
        doc = self.nlp(text)
        triples = []
        for sent in doc.sents:
            nouns = [t.lemma_ for t in sent if t.pos_ == 'NOUN']
            adjs = [t.lemma_ for t in sent if t.pos_ == 'ADJ']
            verbs = [t.lemma_ for t in sent if t.pos_ == 'VERB']
            # Simple cross-product, can be improved
            for n in nouns:
                for a in adjs:
                    for v in verbs:
                        triples.append((n, a, v))
        return triples 