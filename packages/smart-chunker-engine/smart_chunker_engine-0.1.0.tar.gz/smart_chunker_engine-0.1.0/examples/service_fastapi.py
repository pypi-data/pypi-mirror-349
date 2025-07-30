"""
Пример: Smart Chunker Engine как REST API (FastAPI)

- POST /chunk — принимает текст и (опционально) config, возвращает чанки с метаданными
- Для запуска: uvicorn examples.service_fastapi:app --host 0.0.0.0 --port 8000

Пример запроса:
curl -X POST http://localhost:8000/chunk \
  -H "Content-Type: application/json" \
  -d '{"text": "Ваш длинный текст..."}'
"""
from fastapi import FastAPI
from pydantic import BaseModel
from smart_chunker_engine.pipeline import SmartChunkerPipeline
from chunk_metadata_adapter import SemanticChunk
from typing import List, Optional

app = FastAPI(title="Smart Chunker Engine API")
pipeline = SmartChunkerPipeline()

class ChunkRequest(BaseModel):
    text: str
    config: Optional[dict] = None

class ChunkResponse(BaseModel):
    chunks: List[dict]  # SemanticChunk as dict

@app.post("/chunk", response_model=ChunkResponse)
def chunk_text(req: ChunkRequest):
    pipe = pipeline
    if req.config:
        pipe = SmartChunkerPipeline(req.config)
    chunks = pipe.run(req.text)
    return {"chunks": [c.model_dump() for c in chunks]} 