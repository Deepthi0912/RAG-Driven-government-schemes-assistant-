
import json
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[3]

EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

COLLECTION_NAME = "scheme_chunks"
EXPECTED_DIMENSION = 384
BATCH_SIZE = 500


def get_client():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(
        path=str(VECTORSTORE_DIR)
    )


def load_embedding_documents():
    json_files = sorted(
        EMBEDDINGS_DIR.glob("*_embeddings.json")
    )

    if not json_files:
        print("No embedding files found.")
        return []

    documents = []
    seen_ids = set()
    seen_sources = set()

    # Validate every file before changing ChromaDB.
    for json_path in json_files:
        print(f"\nValidating: {json_path.name}")

        with open(json_path, "r", encoding="utf-8") as file:
            document = json.load(file)

        source_file = document["source_file"]
        scheme_id = document.get("scheme_id")

        if source_file in seen_sources:
            raise ValueError(
                f"Duplicate source document: {source_file}"
            )

        seen_sources.add(source_file)

        records = []

        for chunk in document["chunks"]:
            chunk_id = (
                f"{chunk['source_file']}_"
                f"{chunk['page_number']}_"
                f"{chunk['chunk_number']}"
            )

            if chunk_id in seen_ids:
                raise ValueError(
                    f"Duplicate chunk ID: {chunk_id}"
                )

            seen_ids.add(chunk_id)

            embedding = chunk["embedding"]

            if len(embedding) != EXPECTED_DIMENSION:
                raise ValueError(
                    f"Invalid embedding dimension: {chunk_id}"
                )

            metadata = {
                "source_file": chunk["source_file"],
                "page_number": int(chunk["page_number"]),
                "chunk_number": int(chunk["chunk_number"])
            }

            # ChromaDB metadata cannot contain None values.
            if scheme_id is not None:
                metadata["scheme_id"] = int(scheme_id)

            records.append({
                "id": chunk_id,
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": metadata
            })

        documents.append({
            "source_file": source_file,
            "records": records
        })

    return documents


def get_existing_records(collection, source_file):
    return collection.get(
        where={"source_file": source_file},
        include=["documents", "metadatas"]
    )


def document_is_unchanged(existing, records):
    existing_records = {
        chunk_id: (document, metadata)
        for chunk_id, document, metadata in zip(
            existing["ids"],
            existing["documents"],
            existing["metadatas"]
        )
    }

    new_records = {
        record["id"]: (
            record["text"],
            record["metadata"]
        )
        for record in records
    }

    return existing_records == new_records


def update_document(collection, document):
    source_file = document["source_file"]
    records = document["records"]

    existing = get_existing_records(collection, source_file)

    old_ids = set(existing["ids"])
    new_ids = {record["id"] for record in records}

    if document_is_unchanged(existing, records):
        print(f"Unchanged: {source_file}. Skipping.")
        return

    print(f"Updating: {source_file}")

    # Insert/update new records before removing obsolete records.
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start:start + BATCH_SIZE]

        if not batch:
            continue

        collection.upsert(
            ids=[record["id"] for record in batch],
            documents=[record["text"] for record in batch],
            embeddings=[record["embedding"] for record in batch],
            metadatas=[record["metadata"] for record in batch]
        )

    # Remove only obsolete chunks belonging to this document.
    obsolete_ids = old_ids - new_ids

    if obsolete_ids:
        collection.delete(ids=list(obsolete_ids))

    print(f"Chunks available for document: {len(records)}")
    print(f"Obsolete chunks removed: {len(obsolete_ids)}")


def store_embeddings():
    documents = load_embedding_documents()

    if not documents:
        return

    client = get_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    before_count = collection.count()

    print(f"\nExisting ChromaDB chunks: {before_count}")

    for document in documents:
        update_document(collection, document)

    after_count = collection.count()

    print("\nIncremental vector storage completed.")
    print(f"Chunks before update: {before_count}")
    print(f"Chunks after update: {after_count}")
    print(f"Storage location: {VECTORSTORE_DIR}")


if __name__ == "__main__":
    store_embeddings()
