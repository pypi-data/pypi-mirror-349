from smart_chunker_engine.sentence_refine import refine_sentences

def test_refine_sentences_merge_short():
    metablock = ["Hi.", "How are you?", "This is a longer sentence."]
    result = refine_sentences(metablock)
    # Первые два должны слиться, третье отдельно
    assert len(result) == 2
    assert "Hi." in result[0] and "How are you?" in result[0]
    assert "longer sentence" in result[1]

def test_refine_sentences_split_long():
    long_sent = (
        "This is a very long sentence that should be split. "
        "It contains a lot of information and is much longer than the maximum allowed length. "
        "Here is another part that also makes it even longer. "
        "And yet another sentence to ensure we exceed the threshold."
    )
    metablock = [long_sent]
    result = refine_sentences(metablock)
    # Должно быть разбито на несколько частей (минимум 2)
    assert len(result) >= 2
    assert all(len(s) > 0 for s in result)

def test_refine_sentences_normal():
    metablock = ["This is normal length.", "Another normal sentence."]
    result = refine_sentences(metablock)
    assert result == metablock 