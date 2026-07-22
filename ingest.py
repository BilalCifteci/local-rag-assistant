"""Hafta 3: Veri alma (ingestion) pipeline.

docs/ klasörundeki dokümanları paragraf bazlı parçalara (chunk) böler, her
parça için Foundry Local embedding modeliyle vektör üretir ve SQLite'a
(documents.db) kaydeder.
"""

import json
import pathlib
import sqlite3

from foundry_local_sdk import Configuration, FoundryLocalManager

DOCS_DIR = pathlib.Path(__file__).parent / "docs"
DB_PATH = pathlib.Path(__file__).parent / "documents.db"
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"


def chunk_document(text: str) -> list[str]:
    """Dokümanı boş satırlara göre paragraflara böler, çok kısa paragrafları birleştirir."""
    raw_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    buffer = ""
    for paragraph in raw_paragraphs:
        buffer = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph
        if len(buffer) >= 200:
            chunks.append(buffer)
            buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE IF EXISTS chunks")
    conn.execute(
        """
        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )
    conn.commit()


def main() -> None:
    FoundryLocalManager.initialize(Configuration(app_name="local-rag-assistant"))
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model(EMBEDDING_MODEL_ALIAS)
    print(f"Embedding modeli ({EMBEDDING_MODEL_ALIAS}) indiriliyor...")
    model.download(lambda p: print(f"\rIndiriliyor: %{p:.0f}", end="", flush=True))
    print()
    model.load()
    print("Model yuklendi.\n")

    embedding_client = model.get_embedding_client()

    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)

    doc_files = sorted(DOCS_DIR.glob("*.md"))
    if not doc_files:
        raise SystemExit(f"docs/ klasorunde hic dokuman bulunamadi: {DOCS_DIR}")

    total_chunks = 0
    for doc_path in doc_files:
        text = doc_path.read_text(encoding="utf-8")
        chunks = chunk_document(text)
        if not chunks:
            continue

        response = embedding_client.generate_embeddings(chunks)
        vectors = [item.embedding for item in response.data]

        for index, (chunk_text, vector) in enumerate(zip(chunks, vectors)):
            conn.execute(
                "INSERT INTO chunks (source, chunk_index, content, embedding) VALUES (?, ?, ?, ?)",
                (doc_path.name, index, chunk_text, json.dumps(vector)),
            )
        conn.commit()
        total_chunks += len(chunks)
        print(f"  {doc_path.name}: {len(chunks)} parca islendi")

    conn.close()
    model.unload()
    print(f"\nToplam {total_chunks} parca '{DB_PATH.name}' icine kaydedildi.")


if __name__ == "__main__":
    main()
