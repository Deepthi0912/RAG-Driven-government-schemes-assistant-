
import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.query_history import QueryHistory
from app.schemas.history import HistoryResponse


router = APIRouter(
    prefix="/api",
    tags=["Query History"]
)


@router.get("/history", response_model=list[HistoryResponse])
def get_query_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    records = (
        db.query(QueryHistory)
        .filter(QueryHistory.user_id == current_user.id)
        .order_by(QueryHistory.created_at.desc())
        .limit(50)
        .all()
    )

    history = []

    for record in records:

        try:
            sources = json.loads(record.sources_used or "[]")
        except (json.JSONDecodeError, TypeError):
            sources = []

        history.append({
            "id": record.id,
            "question": record.question,
            "answer": record.answer,
            "sources": sources,
            "created_at": record.created_at
        })

    return history
