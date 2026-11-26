
import re
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.db.database import SessionLocal
from app.models.scheme import Scheme


# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

COLLECTION_NAME = "scheme_chunks"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# =========================================================
# LOAD EMBEDDING MODEL AND VECTOR DATABASE
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(value: str) -> str:
    """
    Remove special characters and spaces for matching.
    """

    return re.sub(
        r"[^a-z0-9]+",
        "",
        value.lower()
    )


# =========================================================
# DYNAMIC SCHEME IDENTIFICATION
# =========================================================

def identify_scheme(question: str):
    """
    Identify a scheme dynamically using names stored
    in the PostgreSQL database.

    Also recognizes abbreviations inside parentheses.

    Example:
    Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)
    """

    normalized_question = normalize_text(question)

    db = SessionLocal()

    try:
        schemes = db.query(Scheme).all()

        matches = []

        for scheme in schemes:

            if not scheme.name:
                continue

            candidates = [scheme.name]

            # Extract abbreviations inside parentheses.
            abbreviations = re.findall(
                r"\(([^)]+)\)",
                scheme.name
            )

            candidates.extend(abbreviations)

            for candidate in candidates:

                normalized_candidate = normalize_text(
                    candidate
                )

                if (
                    normalized_candidate
                    and normalized_candidate in normalized_question
                ):

                    matches.append(
                        (scheme, len(normalized_candidate))
                    )

        if not matches:
            return None

        # Prefer the longest matching scheme name.
        matches.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return matches[0][0]

    finally:
        db.close()


# =========================================================
# RETRIEVE RELEVANT DOCUMENT CHUNKS
# =========================================================

def retrieve_relevant_chunks(
    question: str,
    top_k: int = 5
):

    if top_k < 1:
        raise ValueError(
            "top_k must be at least 1."
        )

    # Generate question embedding.
    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # Identify the scheme dynamically.
    scheme = identify_scheme(question)

    query_arguments = {}

    if scheme:

        scheme_filter = {
            "scheme_id": scheme.id
        }

        # ChromaDB compatibility:
        # Count matching records using get(),
        # because Collection.count() does not accept where.
        matching_records = collection.get(
            where=scheme_filter,
            include=["metadatas"]
        )

        available_count = len(
            matching_records["ids"]
        )

        print(
            f"\nDetected scheme: {scheme.name}"
        )

        print(
            f"Scheme ID: {scheme.id}"
        )

        print(
            f"Matching document chunks: {available_count}"
        )

        # Avoid retrieving unrelated scheme documents.
        if available_count == 0:

            print(
                "No indexed documents found for this scheme."
            )

            return []

        query_arguments["where"] = scheme_filter

    else:

        available_count = collection.count()

        print(
            "\nNo specific scheme detected."
        )

        print(
            "Using global document search."
        )

    if available_count == 0:
        return []

    # Search ChromaDB.
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(
            top_k,
            available_count
        ),
        include=[
            "documents",
            "metadatas",
            "distances"
        ],
        **query_arguments
    )

    retrieved_chunks = []

    for index in range(
        len(results["ids"][0])
    ):

        metadata = results["metadatas"][0][index]

        retrieved_chunks.append({

            "text": results["documents"][0][index],

            "source_file": metadata.get(
                "source_file"
            ),

            "page_number": metadata.get(
                "page_number"
            ),

            "chunk_number": metadata.get(
                "chunk_number"
            ),

            "scheme_id": metadata.get(
                "scheme_id"
            ),

            "distance": results["distances"][0][index]

        })

    return retrieved_chunks


# =========================================================
# TEST RETRIEVER
# =========================================================

if __name__ == "__main__":

    test_question = (
        "What are the eligibility criteria for PM-KISAN?"
    )

    chunks = retrieve_relevant_chunks(
        test_question,
        top_k=5
    )

    print(
        f"\nRetrieved {len(chunks)} chunks."
    )

    for chunk in chunks:

        print(
            "\nSource:",
            chunk["source_file"]
        )

        print(
            "Page:",
            chunk["page_number"]
        )

        print(
            "Scheme ID:",
            chunk["scheme_id"]
        )

        print(
            "Text:",
            chunk["text"][:300]
        )
