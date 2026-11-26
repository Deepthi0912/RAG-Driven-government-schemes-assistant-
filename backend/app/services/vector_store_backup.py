
import json
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[3]

EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

COLLECTION_NAME = "scheme_chunks"
EXPECTED_DIMENSION = 384


def get_client():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(
        path=str(VECTORSTORE_DIR)
    )


def store_embeddings():

    json_files = sorted(
        EMBEDDINGS_DIR.glob("*_embeddings.json")
    )

    if not json_files:
        print("No embedding files found.")
        return

    # Load and validate all files BEFORE changing ChromaDB.
    all_ids = []
    all_texts = []
    all_embeddings = []
    all_metadatas = []

    for json_path in json_files:

        print(f"\nLoading: {json_path.name}")

        with open(json_path, "r", encoding="utf-8") as file:
            document = json.load(file)

        for chunk in document["chunks"]:

            chunk_id = (
                f"{chunk['source_file']}_"
                f"{chunk['page_number']}_"
                f"{chunk['chunk_number']}"
            )

            embedding = chunk["embedding"]

            if len(embedding) != EXPECTED_DIMENSION:
                raise ValueError(
                    f"Invalid embedding dimension in {json_path.name}: "
                    f"{len(embedding)}"
                )

            all_ids.append(chunk_id)
            all_texts.append(chunk["text"])
            all_embeddings.append(embedding)

            all_metadatas.append({
                "source_file": chunk["source_file"],
                "page_number": int(chunk["page_number"]),
                "chunk_number": int(chunk["chunk_number"])
            })

    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate chunk IDs found. Aborting rebuild.")

    if not all_ids:
        print("No chunks found. Aborting rebuild.")
        return

    print(f"\nTotal chunks prepared: {len(all_ids)}")
    print("All embedding dimensions validated.")
    print("Chunk IDs are unique.")

    # Rebuild the collection only after validation succeeds.
    client = get_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("\nPrevious collection deleted.")
    except Exception:
        print("\nNo previous collection found. Creating a new one.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    collection.upsert(
        ids=all_ids,
        documents=all_texts,
        embeddings=all_embeddings,
        metadatas=all_metadatas
    )

    final_count = collection.count()

    print("\nVector storage completed.")
    print(f"Files processed: {len(json_files)}")
    print(f"Chunks inserted: {len(all_ids)}")
    print(f"Chunks in collection: {final_count}")
    print(f"Storage location: {VECTORSTORE_DIR}")

    if final_count != len(all_ids):
        raise RuntimeError("Vector-store count verification failed.")

    print("\nSUCCESS: ChromaDB rebuilt and verified.")


if __name__ == "__main__":
    store_embeddings()
