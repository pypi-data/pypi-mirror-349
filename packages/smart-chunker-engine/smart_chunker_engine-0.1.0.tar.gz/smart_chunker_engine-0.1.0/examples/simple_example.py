#!/usr/bin/env python3
"""
Simple example of using the Smart Chunker package.
"""

import sys
from pathlib import Path
import logging

# Add parent directory to import path
sys.path.append(str(Path(__file__).parent.parent))

from chunker.pipeline import ChunkerPipeline


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Text for processing
    text = """
    Искусственный интеллект (ИИ) — это способность компьютерных систем выполнять задачи, 
    которые обычно требуют человеческого интеллекта. Он включает в себя обучение, 
    рассуждение, самокоррекцию и восприятие.
    
    Машинное обучение — это подраздел ИИ, который позволяет системам автоматически 
    учиться и улучшаться на основе опыта. Глубокое обучение, в свою очередь, является 
    специализированной формой машинного обучения, которая использует нейронные сети для 
    моделирования абстракций высокого уровня.
    
    Современные приложения ИИ включают распознавание речи, компьютерное зрение, обработку 
    естественного языка и рекомендательные системы. Многие из этих технологий стали 
    частью нашей повседневной жизни.
    """
    
    # Initialize and run pipeline
    pipeline = ChunkerPipeline()
    result = pipeline.run(text)
    
    # Display results
    print(f"\nProcessing complete. Found {len(result['chunks'])} chunks:\n")
    
    for chunk in result["chunks"]:
        print(f"Chunk {chunk['index']}:")
        print(f"  {chunk['text']}")
        print()
    
    # Save results
    output_file = pipeline.save_result(result)
    print(f"Results saved to {output_file}")

    # --- Export Smart Chunker Engine formats ---
    from smart_chunker_engine.exporter import export_chunks
    from chunk_metadata_adapter import SemanticChunk, FlatSemanticChunk
    from smart_chunker_engine.metadata_builder import MetadataBuilder

    # Преобразуем результат в SemanticChunk и FlatSemanticChunk
    semantic_chunks = []
    flat_chunks = []
    for chunk in result["chunks"]:
        # Пример: преобразуем dict в SemanticChunk через MetadataBuilder (минимальный набор полей)
        semantic = MetadataBuilder.build_semantic_chunk(
            text=chunk["text"],
            start=chunk.get("start", 0),
            end=chunk.get("end", len(chunk["text"])),
            method=chunk.get("method", "hybrid"),
            language="ru",
            type="DocBlock"
        )
        semantic_chunks.append(semantic)
        flat_chunks.append(FlatSemanticChunk.from_semantic_chunk(semantic))

    # Экспортируем в JSON (semantic_chunks.json)
    export_chunks(semantic_chunks, "semantic_chunks.json", format="json")
    print("Exported semantic_chunks.json")

    # Экспортируем в CSV (flat_chunks.csv)
    export_chunks(flat_chunks, "flat_chunks.csv", format="csv")
    print("Exported flat_chunks.csv")

    # Экспортируем в Parquet (если доступен pandas)
    try:
        export_chunks(flat_chunks, "flat_chunks.parquet", format="parquet")
        print("Exported flat_chunks.parquet")
    except ImportError:
        print("[INFO] pandas not installed: Parquet export skipped.")


if __name__ == "__main__":
    main() 