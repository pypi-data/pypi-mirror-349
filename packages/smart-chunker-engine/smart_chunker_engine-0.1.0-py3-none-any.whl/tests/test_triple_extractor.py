import pytest
from smart_chunker_engine.triple_extractor import TripleExtractor

UD_PATH = "data/large_datasets/ru_gsd-ud-test.conllu"

def get_first_n_sentences_conllu(path, n=10):
    sentences = []
    with open(path, encoding="utf-8") as f:
        sent = []
        for line in f:
            if line.startswith("#"):
                continue
            if line.strip() == "":
                if sent:
                    sentences.append(" ".join(sent))
                    sent = []
                    if len(sentences) >= n:
                        break
                continue
            cols = line.strip().split("\t")
            if len(cols) > 1:
                sent.append(cols[1])
    return sentences

def test_triple_extractor_smoke():
    """Smoke test for TripleExtractor instantiation and extract method signature."""
    extractor = TripleExtractor()
    result = extractor.extract("Тестовый текст.")
    assert isinstance(result, list)

@pytest.mark.parametrize("text", get_first_n_sentences_conllu(UD_PATH, 10))
def test_triple_extractor_ud(text):
    extractor = TripleExtractor()
    triples = extractor.extract(text)
    assert isinstance(triples, list)
    # Можно добавить assert на структуру троек, если нужно 