import unittest
from smart_chunker_engine.initial_split import InitialSplitter
from chunk_metadata_adapter.models import SemanticChunk

class TestInitialSplitter(unittest.TestCase):
    def test_basic_split(self):
        text = "a" * 1200
        splitter = InitialSplitter(chunk_size=500)
        chunks = splitter.split(text)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(isinstance(c, SemanticChunk) for c in chunks))
        self.assertEqual(chunks[0].text, "a" * 500)
        self.assertEqual(chunks[1].text, "a" * 500)
        self.assertEqual(chunks[2].text, "a" * 200)

    def test_overlap(self):
        text = "abcdefghij" * 100  # 1000 chars
        splitter = InitialSplitter(chunk_size=300, overlap=100)
        chunks = splitter.split(text)
        self.assertGreater(len(chunks), 3)
        # Check overlap
        for i in range(1, len(chunks)):
            overlap = len(set(chunks[i-1].text[-100:]) & set(chunks[i].text[:100]))
            self.assertGreaterEqual(overlap, 1)

    def test_empty_and_invalid(self):
        splitter = InitialSplitter(chunk_size=500)
        self.assertEqual(splitter.split(""), [])
        splitter = InitialSplitter(chunk_size=0)
        self.assertEqual(splitter.split("abc"), [])

    def test_config_override(self):
        text = "x" * 600
        config = {"chunk_size": 200, "language": "en"}
        splitter = InitialSplitter(config=config)
        chunks = splitter.split(text)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(c.language == "en" for c in chunks))

if __name__ == "__main__":
    unittest.main() 