
import json
import hashlib
from pathlib import Path

from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def calculate_hash(file_path: Path):
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def same_chunks(old_chunks, new_chunks):
    """Compare chunk content and scheme association."""

    fields = (
        "source_file",
        "scheme_id",
        "page_number",
        "chunk_number",
        "text"
    )

    if len(old_chunks) != len(new_chunks):
        return False

    for old, new in zip(old_chunks, new_chunks):
        if any(old.get(field) != new.get(field) for field in fields):
            return False

        embedding = old.get("embedding")

        if not isinstance(embedding, list) or len(embedding) != 384:
            return False

    return True


def generate_embeddings():
    json_files = sorted(CHUNKS_DIR.glob("*_chunks.json"))

    if not json_files:
        print("No chunk files found.")
        return

    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    model = None

    for json_path in json_files:
        print(f"\nChecking: {json_path.name}")

        with open(json_path, "r", encoding="utf-8") as file:
            document = json.load(file)

        chunks = document["chunks"]
        chunks_hash = calculate_hash(json_path)
        scheme_id = document.get("scheme_id")

        output_file = (
            EMBEDDINGS_DIR /
            f"{json_path.stem.replace('_chunks', '')}_embeddings.json"
        )

        if output_file.exists():
            try:
                with open(output_file, "r", encoding="utf-8") as file:
                    existing = json.load(file)

                if (
                    existing.get("model") == MODEL_NAME
                    and same_chunks(existing.get("chunks", []), chunks)
                ):
                    if existing.get("chunks_sha256") != chunks_hash:
                        existing["chunks_sha256"] = chunks_hash

                        with open(output_file, "w", encoding="utf-8") as file:
                            json.dump(existing, file, ensure_ascii=False)

                    print("Chunks unchanged. Existing embeddings preserved.")
                    continue

            except (json.JSONDecodeError, OSError, TypeError):
                print("Existing embeddings invalid. Regenerating.")

        print("New or modified chunks. Generating embeddings...")

        if model is None:
            print("Loading embedding model...")
            model = SentenceTransformer(MODEL_NAME)

        texts = [chunk["text"] for chunk in chunks]

        vectors = model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        embedded_chunks = []

        for chunk, vector in zip(chunks, vectors):
            embedded_chunks.append({
                **chunk,
                "embedding": vector.tolist()
            })

        output_data = {
            "source_file": document["source_file"],
            "scheme_id": scheme_id,
            "model": MODEL_NAME,
            "chunks_sha256": chunks_hash,
            "embedding_dimension": model.get_sentence_embedding_dimension(),
            "total_chunks": len(embedded_chunks),
            "chunks": embedded_chunks
        }

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False)

        print(f"Generated embeddings: {len(embedded_chunks)}")
        print(f"Scheme ID: {scheme_id}")
        print(f"Saved to: {output_file}")

    print("\nEmbedding generation completed.")


if __name__ == "__main__":
    generate_embeddings()
