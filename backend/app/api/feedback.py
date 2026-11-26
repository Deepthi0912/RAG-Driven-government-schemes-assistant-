
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.query_history import QueryHistory
from app.models.feedback import Feedback

from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse
)


router = APIRouter(
    prefix="/api",
    tags=["Feedback"]
)


@router.post(
    "/feedback",
    response_model=FeedbackResponse
)
def submit_feedback(
    request: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.id == request.query_id,
            QueryHistory.user_id == current_user.id
        )
        .first()
    )

    if not query:
        raise HTTPException(
            status_code=404,
            detail="Query history not found."
        )

    feedback = Feedback(
        query_id=request.query_id,
        user_id=current_user.id,
        rating=request.rating,
        comment=request.comment
    )

    try:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save feedback."
        )
