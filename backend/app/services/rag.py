from __future__ import annotations
from typing import List, Dict, Any, Optional
from chromadb import PersistentClient
from ..config import CHROMA_DIR

_client: Optional[PersistentClient] = None
_collection = None


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(name="dhristri")
    return _collection


def upsert(video_id: str, start: int, end: int, text: str, embedding: List[float]) -> None:
    col = get_collection()
    col.upsert(
        ids=[f"{video_id}:{start}"],
        embeddings=[embedding],
        metadatas=[{"videoId": video_id, "startSec": start, "endSec": end}],
        documents=[text],
    )


def search(video_id: str, query_embedding: List[float], k: int = 5) -> Dict[str, Any]:
    col = get_collection()
    return col.query(query_embeddings=[query_embedding], n_results=k, where={"videoId": video_id})


