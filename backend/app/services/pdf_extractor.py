
from pathlib import Path
import hashlib
import json

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def calculate_hash(file_path: Path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def extract_text_from_pdf(pdf_path: Path):

    reader = PdfReader(str(pdf_path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return extracted_pages


def process_pdf(pdf_path: Path):

    print(f"\nProcessing: {pdf_path.name}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / f"{pdf_path.stem}.json"

    current_hash = calculate_hash(pdf_path)

    # Skip extraction when the PDF has not changed.
    if output_file.exists():

        try:
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

            if existing_data.get("source_sha256") == current_hash:
                print("PDF unchanged. Skipping extraction.")
                return existing_data

        except (json.JSONDecodeError, OSError):
            print("Existing processed file is invalid. Re-extracting.")

    pages = extract_text_from_pdf(pdf_path)

    reader = PdfReader(str(pdf_path))

    full_text = "\n".join(
        page["text"] for page in pages
    )

    output_data = {
        "source_file": pdf_path.name,
        "source_sha256": current_hash,
        "total_pages": len(reader.pages),
        "extracted_pages": len(pages),
        "total_characters": len(full_text),
        "pages": pages
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            output_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"Total pages: {output_data['total_pages']}")
    print(f"Pages with text: {output_data['extracted_pages']}")
    print(f"Extracted characters: {output_data['total_characters']}")
    print(f"Saved to: {output_file}")

    return output_data


def process_all_pdfs():

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:

        try:
            process_pdf(pdf_path)

        except Exception as error:
            print(f"Failed to process {pdf_path.name}: {error}")


if __name__ == "__main__":
    process_all_pdfs()

from pathlib import Path
import hashlib
import json

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def calculate_hash(file_path: Path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def extract_text_from_pdf(pdf_path: Path):

    reader = PdfReader(str(pdf_path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return extracted_pages


def process_pdf(pdf_path: Path, scheme_id: int | None = None):

    print(f"\nProcessing: {pdf_path.name}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / f"{pdf_path.stem}.json"

    current_hash = calculate_hash(pdf_path)

    if output_file.exists():

        try:
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

            if (
                existing_data.get("source_sha256") == current_hash
                and existing_data.get("scheme_id") == scheme_id
            ):
                print("PDF unchanged. Skipping extraction.")
                return existing_data

        except (json.JSONDecodeError, OSError):
            print("Existing processed file is invalid. Re-extracting.")

    pages = extract_text_from_pdf(pdf_path)

    reader = PdfReader(str(pdf_path))

    full_text = "\n".join(
        page["text"] for page in pages
    )

    output_data = {
        "source_file": pdf_path.name,
        "scheme_id": scheme_id,
        "source_sha256": current_hash,
        "total_pages": len(reader.pages),
        "extracted_pages": len(pages),
        "total_characters": len(full_text),
        "pages": pages
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            output_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"Total pages: {output_data['total_pages']}")
    print(f"Pages with text: {output_data['extracted_pages']}")
    print(f"Scheme ID: {scheme_id}")
    print(f"Saved to: {output_file}")

    return output_data


def process_all_pdfs():

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:

        try:
            process_pdf(pdf_path)

        except Exception as error:
            print(f"Failed to process {pdf_path.name}: {error}")


if __name__ == "__main__":
    process_all_pdfs()
