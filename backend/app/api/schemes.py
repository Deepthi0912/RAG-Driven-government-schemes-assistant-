
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.document import Document
from app.db.dependencies import get_db
from app.models.scheme import Scheme
from app.models.category import Category
from app.models.user import User
from app.schemas.scheme import (
    SchemeCreate,
    SchemeResponse
)
from app.core.auth import get_current_admin_user


router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)


@router.post(
    "",
    response_model=SchemeResponse
)
def create_scheme(
    scheme: SchemeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    category = (
        db.query(Category)
        .filter(Category.id == scheme.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_scheme = (
        db.query(Scheme)
        .filter(Scheme.name == scheme.name)
        .first()
    )

    if existing_scheme:
        raise HTTPException(
            status_code=400,
            detail="Scheme already exists"
        )

    new_scheme = Scheme(
        category_id=scheme.category_id,
        name=scheme.name,
        description=scheme.description,
        ministry=scheme.ministry,
        official_url=scheme.official_url
    )

    db.add(new_scheme)
    db.commit()
    db.refresh(new_scheme)

    return new_scheme


@router.get(
    "",
    response_model=list[SchemeResponse]
)
def get_schemes(
    db: Session = Depends(get_db)
):
    return db.query(Scheme).all()


@router.get(
    "/{scheme_id}",
    response_model=SchemeResponse
)
def get_scheme(
    scheme_id: int,
    db: Session = Depends(get_db)
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

    return scheme


@router.delete("/{scheme_id}")
def delete_scheme(
    scheme_id: int,
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

    # Prevent deletion if documents are linked to this scheme
    linked_documents = (
        db.query(Document)
        .filter(Document.scheme_id == scheme_id)
        .first()
    )

    if linked_documents:
        raise HTTPException(
            status_code=400,
            detail="Please remove linked documents before deleting this scheme"
        )

    db.delete(scheme)
    db.commit()

    return {
        "message": "Scheme deleted successfully",
        "scheme_id": scheme_id
    }