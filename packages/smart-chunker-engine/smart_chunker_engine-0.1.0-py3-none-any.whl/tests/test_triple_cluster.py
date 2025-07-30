import pytest
from smart_chunker_engine.triple_cluster import TripleCluster
from smart_chunker_engine.triple_extractor import TripleExtractor

UD_PATH = "data/large_datasets/ru_gsd-ud-test.conllu"

# Ограничиваем количество троек для теста и размер батча
MAX_TRIPLES = 10
BATCH_SIZE = 10

def get_triples_from_ud(path, n=10):
    from smart_chunker_engine.triple_extractor import TripleExtractor
    extractor = TripleExtractor()
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
    triples = []
    for text in sentences:
        triples.extend(extractor.extract(text))
    return triples[:max(n, 5)]  # min_cluster_size=5

def test_triple_cluster_smoke():
    """Smoke test for TripleCluster instantiation and cluster method signature."""
    clusterer = TripleCluster(device='cpu', batch_size=BATCH_SIZE)
    triples = [("N", "A", "V")] * 5  # min_cluster_size=5
    result = clusterer.cluster(triples)
    assert isinstance(result, dict)

@pytest.mark.skipif(len(get_triples_from_ud(UD_PATH, MAX_TRIPLES)) < 5, reason="Not enough triples in sample")
def test_triple_cluster_ud():
    clusterer = TripleCluster(device='cpu', batch_size=BATCH_SIZE)
    triples = get_triples_from_ud(UD_PATH, MAX_TRIPLES)
    result = clusterer.cluster(triples)
    assert isinstance(result, dict)
    assert len(result) > 0 