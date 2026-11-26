
from pathlib import Path
import shutil
import traceback

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.database import SessionLocal
from app.models.document import Document
from app.models.scheme import Scheme
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.core.auth import get_current_admin_user


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PROJECT_ROOT / "data" / "raw"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def process_uploaded_document(document_id: int):
    """Process an uploaded PDF through the RAG pipeline."""

    db = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return

        document.processing_status = "processing"
        db.commit()

        pdf_path = Path(document.file_path)
        scheme_id = document.scheme_id

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"Uploaded PDF not found: {pdf_path}"
            )

        from app.services.pdf_extractor import (
            process_pdf,
            PROCESSED_DIR
        )

        from app.services.text_processor import (
            process_json_file,
            CHUNKS_DIR
        )

        from app.services.embedding_generator import (
            generate_embeddings
        )

        from app.services.vector_store import (
            store_embeddings
        )

        # 1. Extract PDF text and attach scheme ID.
        print(f"Extracting PDF: {pdf_path.name}")
        print(f"Associated scheme ID: {scheme_id}")

        extracted_data = process_pdf(
            pdf_path,
            scheme_id=scheme_id
        )

        if extracted_data["extracted_pages"] == 0:
            raise ValueError(
                "No readable text found in this PDF."
            )

        # 2. Create chunks.
        processed_path = (
            PROCESSED_DIR / f"{pdf_path.stem}.json"
        )

        process_json_file(processed_path)

        chunks_path = (
            CHUNKS_DIR / f"{pdf_path.stem}_chunks.json"
        )

        if not chunks_path.exists():
            raise FileNotFoundError(
                "Chunk file was not generated."
            )

        # 3. Generate embeddings.
        print(f"Generating embeddings: {pdf_path.name}")
        generate_embeddings()

        # 4. Store/update ChromaDB.
        print(f"Updating ChromaDB: {pdf_path.name}")
        store_embeddings()

        # 5. Mark document as processed.
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document:
            document.processing_status = "processed"
            db.commit()

        print(f"Successfully processed: {pdf_path.name}")

    except Exception as error:
        db.rollback()

        print(f"Document processing failed: {error}")
        traceback.print_exc()

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document:
            document.processing_status = "failed"
            db.commit()

    finally:
        db.close()


@router.post(
    "/upload/{scheme_id}",
    response_model=DocumentResponse
)
def upload_document(
    scheme_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    scheme = (
        db.query(Scheme)
        .filter(Scheme.id == scheme_id)
        .first()
    )

    if not scheme:
        raise HTTPException(
            status_code=404,
            detail="Scheme not found"
        )

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    safe_filename = Path(
        file.filename.replace("\\", "/")
    ).name

    file_path = UPLOAD_DIR / safe_filename

    if file_path.exists():
        raise HTTPException(
            status_code=409,
            detail="A file with this name already exists. Please rename the PDF."
        )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            scheme_id=scheme_id,
            file_name=safe_filename,
            file_path=str(file_path),
            processing_status="pending"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        background_tasks.add_task(
            process_uploaded_document,
            document.id
        )

        return document

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise

    finally:
        file.file.close()


@router.get(
    "",
    response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return (
        db.query(Document)
        .order_by(Document.uploaded_at.desc())
        .all()
    )
