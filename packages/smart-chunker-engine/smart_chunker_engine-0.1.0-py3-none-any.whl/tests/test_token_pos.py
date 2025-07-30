import pytest
from smart_chunker_engine.token_pos import filter_pos_tokens

def test_filter_pos_tokens_spacy(monkeypatch):
    class DummyToken:
        def __init__(self, text, pos_):
            self.text = text
            self.pos_ = pos_
    class DummyDoc(list):
        pass
    def dummy_nlp(text):
        return DummyDoc([
            DummyToken("Apple", "NOUN"),
            DummyToken("is", "VERB"),
            DummyToken("red", "ADJ"),
            DummyToken("and", "CONJ"),
            DummyToken("juicy", "ADJ"),
        ])
    monkeypatch.setattr("smart_chunker_engine.token_pos._nlp", dummy_nlp)
    tokens = filter_pos_tokens("Apple is red and juicy")
    assert tokens == ["Apple", "is", "red", "juicy"]

def test_filter_pos_tokens_fallback(monkeypatch):
    monkeypatch.setattr("smart_chunker_engine.token_pos._nlp", None)
    tokens = filter_pos_tokens("Apple is red and juicy")
    assert tokens == ["Apple", "is", "red", "and", "juicy"] 