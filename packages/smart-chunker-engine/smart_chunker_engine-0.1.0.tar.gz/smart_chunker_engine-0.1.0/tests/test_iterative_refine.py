import pytest
from smart_chunker_engine.iterative_refine import IterativeRefiner

def test_iterative_refiner_smoke():
    """Smoke test for IterativeRefiner instantiation and refine method signature."""
    refiner = IterativeRefiner()
    result = refiner.refine([{"text": "chunk1"}, {"text": "chunk2"}])
    assert isinstance(result, list)

def test_refine_skip_short():
    """Short chunks (<20 символов, <2 предложений) должны возвращаться без изменений."""
    short_chunks = [
        {'text': 'Short.'},
        {'text': 'Another.'},
    ]
    refiner = IterativeRefiner(lambda_=0.4, theta_high=0.1, theta_low=0.01, epsilon=1e-3, max_iter=2)
    out = refiner.refine(list(short_chunks))
    assert out == short_chunks
    # Один длинный, один короткий — тоже не должно быть merge
    mixed = [
        {'text': 'Short.'},
        {'text': 'This is a long enough chunk. It has two sentences.'},
    ]
    out2 = refiner.refine(list(mixed))
    assert out2 == mixed

def test_refine_apply_realistic():
    """Длинные чанки с несколькими предложениями должны подвергаться split/merge."""
    chunks = [
        {'text': 'The cat sat on the mat. The cat purred.'},
        {'text': 'A cat is sitting on a mat. It looks happy.'},
        {'text': 'The dog barked loudly. The dog ran away.'},
    ]
    refiner = IterativeRefiner(lambda_=0.4, theta_high=0.1, theta_low=0.9, epsilon=1e-3, max_iter=2)
    out = refiner.refine(list(chunks))
    # Должно быть не больше исходного, но split/merge возможны
    assert 1 <= len(out) <= 3
    # Должен быть хотя бы один чанк длиннее 30 символов (merge)
    assert any(len(c['text']) > 30 for c in out)

def test_refine_merge_split():
    """Test greedy MERGE/SPLIT logic with длинными чанками (>=20 символов, >=2 предложений)."""
    chunks = [
        {'text': 'The cat sat on the mat. The cat purred softly.'},
        {'text': 'A cat is sitting on a mat. It looks happy and calm.'},
        {'text': 'The dog barked loudly. The dog ran away quickly.'},
    ]
    refiner = IterativeRefiner(lambda_=0.4, theta_high=0.1, theta_low=0.9, epsilon=1e-3, max_iter=2)
    # With low theta_high, merge возможен (все в один чанк)
    out = refiner.refine(list(chunks))
    assert 1 <= len(out) <= 3
    # With high theta_high, merge невозможен
    refiner2 = IterativeRefiner(lambda_=0.4, theta_high=0.99, theta_low=0.9, epsilon=1e-3, max_iter=2)
    out2 = refiner2.refine(list(chunks))
    assert len(out2) == 3

def test_refine_empty_and_single():
    """Test refine with empty and single chunk input."""
    refiner = IterativeRefiner()
    assert refiner.refine([]) == []
    assert refiner.refine([{'text': 'abc'}]) == [{'text': 'abc'}]

def test_split_logic():
    """Test that SPLIT is triggered for low cohesion (realistic multi-sentence chunk)."""
    chunk = {'text': 'This is the first sentence. This is the second sentence.'}
    refiner = IterativeRefiner(lambda_=0.4, theta_high=0.9, theta_low=0.5, epsilon=1e-3, max_iter=2)
    out = refiner.refine([chunk, {'text': 'Another chunk.'}])
    # Должен появиться чанк длиной < исходного (split)
    assert any(len(c['text']) < len(chunk['text']) for c in out)

def test_split_short_chunk():
    """SPLIT невозможен для коротких чанков (<2 предложений)."""
    chunk = {'text': 'Short'}
    refiner = IterativeRefiner(lambda_=0.4, theta_high=0.9, theta_low=0.01, epsilon=1e-3, max_iter=2)
    out = refiner.refine([chunk, {'text': 'Another'}])
    # Не должно появиться чанков короче исходного
    assert all(len(c['text']) >= len(chunk['text']) for c in out) 