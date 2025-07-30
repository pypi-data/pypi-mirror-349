"""
pipeline.py

Main pipeline for Smart Chunker Engine.
Implements the full text-to-chunks flow as specified in docs/7.md and implementation_plan.md.
All metadata operations use chunk_metadata_adapter (>=1.3.0).

Public API:
    SmartChunkerPipeline.run(text: str, config: dict = None) -> list[SemanticChunk]
"""
from typing import List, Optional, Dict, Any
from chunk_metadata_adapter import SemanticChunk
from smart_chunker_engine.pre_normalize import PreNormalizer
from smart_chunker_engine.initial_split import InitialSplitter
from smart_chunker_engine.token_pos import filter_pos_tokens
from smart_chunker_engine.boundary_segmenter import BoundarySegmenter
from smart_chunker_engine.stats_gate import StatsGate
from smart_chunker_engine.triple_extractor import TripleExtractor
from smart_chunker_engine.triple_cluster import TripleCluster
from smart_chunker_engine.tfidf_layer import TfidfLayer
from smart_chunker_engine.metablock import MetablockSegmenter
from smart_chunker_engine.sentence_refine import refine_sentences
from smart_chunker_engine.iterative_refine import IterativeRefiner
from smart_chunker_engine.metadata_builder import MetadataBuilder
from smart_chunker_engine.exporter import export_chunks

class SmartChunkerPipeline:
    """Full pipeline for semantic chunking and metadata generation."""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.normalizer = PreNormalizer(self.config.get('normalize'))
        self.splitter = InitialSplitter(config=self.config.get('split'))
        self.boundary = BoundarySegmenter(**(self.config.get('boundary') or {}))
        self.stats_gate = StatsGate(**(self.config.get('stats_gate') or {}))
        self.triple_extractor = TripleExtractor(self.config.get('spacy_model', 'ru_core_news_md'))
        self.triple_cluster = TripleCluster(**(self.config.get('triple_cluster') or {}))
        self.tfidf_layer = TfidfLayer(**(self.config.get('tfidf') or {}))
        self.metablock = MetablockSegmenter(**(self.config.get('metablock') or {}))
        self.iter_refine = IterativeRefiner(**(self.config.get('iter_refine') or {}))
        self.metadata_builder = MetadataBuilder()

    def run(self, text: str) -> List[SemanticChunk]:
        """Run the full chunking pipeline on input text.

        Args:
            text (str): Raw input text.
        Returns:
            List[SemanticChunk]: List of chunk metadata objects.
        """
        # 1. Pre-normalization
        norm_text = self.normalizer.normalize(text)
        # 2. Initial split (hybrid/fixed)
        initial_chunks = self.splitter.split(norm_text)
        # Преобразуем в dict для промежуточных этапов
        chunks = [{'text': c.text} for c in initial_chunks if c.text.strip()]
        if not chunks:
            return []
        # 3. POS-filter tokens for each chunk
        for chunk in chunks:
            chunk['tokens'] = filter_pos_tokens(chunk['text'])
        # 4. Boundary detection (SBERT window)
        for chunk in chunks:
            chunk['boundaries'] = self.boundary.segment(chunk['tokens'])
        # 5. Stats gate: enable TF-IDF?
        for chunk in chunks:
            chunk['enable_tfidf'] = self.stats_gate.should_enable(chunk['tokens'])
        # 6. Triple extraction & clustering
        for chunk in chunks:
            chunk['triples'] = self.triple_extractor.extract(chunk['text'])
            chunk['token_weights'] = self.triple_cluster.cluster(chunk['triples'])
        # 7. TF-IDF layer (if enabled)
        for chunk in chunks:
            if chunk['enable_tfidf']:
                chunk['tfidf'] = self.tfidf_layer.compute(chunk['tokens'], chunk['token_weights'])
            else:
                chunk['tfidf'] = {}
        # 8. Metablock segmentation
        metablocks = self.metablock.split([{'text': c['text']} for c in chunks])
        # 9. Sentence refinement inside metablocks
        for mb in metablocks:
            mb['refined'] = refine_sentences([c['text'] for c in mb['chunks']])
        # 10. Iterative MERGE/SPLIT refinement
        refined_chunks = []
        for mb in metablocks:
            chunk_dicts = [{'text': s} for s in mb['refined']]
            refined = self.iter_refine.refine(chunk_dicts)
            refined_chunks.extend(refined)
        # 11. Build SemanticChunk metadata
        semantic_chunks = []
        offset = 0
        for c in refined_chunks:
            text = c['text']
            start = offset
            end = offset + len(text)
            semantic_chunk = self.metadata_builder.build_semantic_chunk(
                text=text,
                start=start,
                end=end,
                method="smart_chunker_pipeline"
            )
            semantic_chunks.append(semantic_chunk)
            offset = end
        return semantic_chunks

# Example usage (RU):
# from smart_chunker_engine.pipeline import SmartChunkerPipeline
# pipeline = SmartChunkerPipeline()
# chunks = pipeline.run(raw_text)
# export_chunks(chunks, "output/chunks.json", format="json") 