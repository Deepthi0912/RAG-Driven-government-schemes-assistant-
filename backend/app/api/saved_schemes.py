from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException

from app.db.dependencies import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.saved_scheme import SavedScheme


router = APIRouter(
    prefix="/api/saved-schemes",
    tags=["Saved Schemes"]
)


class SavedSchemeCreate(BaseModel):
    scheme_id: str = Field(
        min_length=1,
        max_length=50
    )


@router.get("/")
def get_saved_schemes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    saved_schemes = (
        db.query(SavedScheme)
        .filter(SavedScheme.user_id == current_user.id)
        .order_by(SavedScheme.created_at.desc())
        .all()
    )

    return {
        "saved_schemes": [
            {
                "scheme_id": item.scheme_code,
                "saved_at": item.created_at
            }
            for item in saved_schemes
        ]
    }


@router.post("/")
def save_scheme(
    request: SavedSchemeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme_code = request.scheme_id.strip().upper()

    if not scheme_code:
        raise HTTPException(
            status_code=400,
            detail="Scheme ID cannot be empty"
        )

    existing = (
        db.query(SavedScheme)
        .filter(
            SavedScheme.user_id == current_user.id,
            SavedScheme.scheme_code == scheme_code
        )
        .first()
    )

    if existing:
        return {
            "message": "Scheme is already saved",
            "scheme_id": scheme_code
        }

    saved_scheme = SavedScheme(
        user_id=current_user.id,
        scheme_code=scheme_code
    )

    db.add(saved_scheme)

    try:
        db.commit()
        db.refresh(saved_scheme)

    except IntegrityError:
        db.rollback()

        return {
            "message": "Scheme is already saved",
            "scheme_id": scheme_code
        }

    return {
        "message": "Scheme saved successfully",
        "scheme_id": scheme_code
    }


@router.delete("/{scheme_id}")
def remove_saved_scheme(
    scheme_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme_code = scheme_id.strip().upper()

    saved_scheme = (
        db.query(SavedScheme)
        .filter(
            SavedScheme.user_id == current_user.id,
            SavedScheme.scheme_code == scheme_code
        )
        .first()
    )

    if not saved_scheme:
        raise HTTPException(
            status_code=404,
            detail="Saved scheme not found"
        )

    db.delete(saved_scheme)
    db.commit()

    return {
        "message": "Scheme removed from saved schemes",
        "scheme_id": scheme_code
    }