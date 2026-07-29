"""Hafta 3: Sorgu icin en alakali dokuman parcalarini bulan retrieval fonksiyonu.

get_top_chunks(query, k) sorguyu embed eder, SQLite'daki tum parca
embedding'leriyle kosinus benzerligi hesaplar ve en alakali k parcayi
dondurur. Kucuk veri setleri icin (bu projede birkac onlarca parca) tum
vektorleri belleye alip karsilastirmak yeterlidir.
"""

import json
import math
import pathlib
import sqlite3
from dataclasses import dataclass

from foundry_local_sdk import Configuration, FoundryLocalManager

DB_PATH = pathlib.Path(__file__).parent / "documents.db"
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"

_manager = None
_embedding_model = None


@dataclass
class RetrievedChunk:
    source: str
    content: str
    similarity: float


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def _get_embedding_model():
    """Foundry Local embedding modelini bir kere baslatip yeniden kullanir."""
    global _manager, _embedding_model
    if _embedding_model is not None:
        return _embedding_model

    if FoundryLocalManager.instance is None:
        FoundryLocalManager.initialize(Configuration(app_name="local-rag-assistant"))
    _manager = FoundryLocalManager.instance

    model = _manager.catalog.get_model(EMBEDDING_MODEL_ALIAS)
    model.download()
    model.load()
    _embedding_model = model
    return model


def get_top_chunks(query: str, k: int = 3) -> list[RetrievedChunk]:
    """Sorgu icin SQLite'daki en alakali k dokuman parcasini dondurur."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"{DB_PATH.name} bulunamadi. Once 'python ingest.py' calistirilmali."
        )

    model = _get_embedding_model()
    query_vector = model.get_embedding_client().generate_embedding(query).data[0].embedding

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT source, content, embedding FROM chunks").fetchall()
    conn.close()

    scored = [
        RetrievedChunk(
            source=source,
            content=content,
            similarity=cosine_similarity(query_vector, json.loads(embedding_json)),
        )
        for source, content, embedding_json in rows
    ]
    scored.sort(key=lambda c: c.similarity, reverse=True)
    return scored[:k]


if __name__ == "__main__":
    test_query = "RAG nedir ve neden kullanilir?"
    print(f"Sorgu: {test_query}\n")
    for chunk in get_top_chunks(test_query):
        print(f"[{chunk.source}] benzerlik={chunk.similarity:.4f}")
        print(chunk.content[:150].replace("\n", " ") + "...\n")
