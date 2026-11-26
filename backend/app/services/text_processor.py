
import json
import re
import hashlib
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def create_chunks(document: dict):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    scheme_id = document.get("scheme_id")

    for page in document["pages"]:
        cleaned_text = clean_text(page["text"])

        if not cleaned_text:
            continue

        page_chunks = splitter.split_text(cleaned_text)

        for chunk_number, chunk_text in enumerate(page_chunks, start=1):
            chunks.append({
                "source_file": document["source_file"],
                "scheme_id": scheme_id,
                "page_number": page["page_number"],
                "chunk_number": chunk_number,
                "text": chunk_text
            })

    return chunks


def process_json_file(json_path: Path):
    print(f"\nChecking: {json_path.name}")

    with open(json_path, "r", encoding="utf-8") as file:
        document = json.load(file)

    source_hash = document.get("source_sha256")

    if not source_hash:
        source_hash = hashlib.sha256(
            json_path.read_bytes()
        ).hexdigest()

    scheme_id = document.get("scheme_id")

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    output_file = CHUNKS_DIR / f"{json_path.stem}_chunks.json"

    # Skip only when both PDF content and scheme association are unchanged.
    if output_file.exists():
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                existing = json.load(file)

            if (
                existing.get("source_sha256") == source_hash
                and existing.get("scheme_id") == scheme_id
            ):
                print("Source and scheme unchanged. Skipping chunk creation.")
                return

        except (json.JSONDecodeError, OSError):
            print("Existing chunk file invalid. Reprocessing.")

    chunks = create_chunks(document)

    output_data = {
        "source_file": document["source_file"],
        "scheme_id": scheme_id,
        "source_sha256": source_hash,
        "total_chunks": len(chunks),
        "chunks": chunks
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

    print(f"Total chunks: {len(chunks)}")
    print(f"Scheme ID: {scheme_id}")
    print(f"Saved to: {output_file}")


def process_all_documents():
    json_files = sorted(PROCESSED_DIR.glob("*.json"))

    if not json_files:
        print("No extracted JSON files found.")
        return

    for json_path in json_files:
        try:
            process_json_file(json_path)
        except Exception as error:
            print(f"Failed: {json_path.name} - {error}")


if __name__ == "__main__":
    process_all_documents()
