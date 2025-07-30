import os
import pytest
from smart_chunker_engine.iterative_refine import IterativeRefiner

@pytest.mark.parametrize('lang,model,fname', [
    ('en', 'all-MiniLM-L6-v2', 'data/input/ud/en_test.conllu'),
    ('ru', 'paraphrase-multilingual-MiniLM-L12-v2', 'data/input/ud/ru_test.conllu'),
    ('uk', 'paraphrase-multilingual-MiniLM-L12-v2', 'data/input/ud/uk_test.conllu'),
])
def test_refine_on_ud(lang, model, fname):
    # Ensure data is downloaded
    assert os.path.exists(fname), f"Missing {fname}"
    # Parse sentences from UD
    sents = []
    with open(fname, encoding='utf8') as f:
        for line in f:
            if line.startswith('# text = '):
                sents.append(line[len('# text = '):].strip())
    # Ограничим для скорости
    sents = sents[:100]
    # Формируем искусственные чанки (по 1 предложению)
    chunks = [{'text': s} for s in sents]
    refiner = IterativeRefiner(model_name=model)
    out = refiner.refine(list(chunks))
    # Инварианты: не пусто, не больше исходного, тексты не пустые
    assert out
    assert len(out) <= len(chunks)
    for ch in out:
        assert ch['text'].strip() 