
import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.qa import AskRequest, AskResponse
from app.services.answer_generator import generate_answer

from app.db.dependencies import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.query_history import QueryHistory


router = APIRouter(
    prefix="/api",
    tags=["AI Assistant"]
)


@router.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        # Generate answer using the existing RAG pipeline
        result = generate_answer(question)

        # Save question, answer and sources in PostgreSQL
        history_record = QueryHistory(
            user_id=current_user.id,
            question=question,
            answer=result["answer"],
            sources_used=json.dumps(result["sources"])
        )

        db.add(history_record)
        db.commit()
        db.refresh(history_record)

        return AskResponse(
    query_id=history_record.id,
    answer=result["answer"],
    sources=result["sources"],
    timings=result["timings"]
)

    except Exception as error:
        db.rollback()

        print("QA API error:", error)

        raise HTTPException(
            status_code=500,
            detail="SchemeWise could not process your question."
        )
