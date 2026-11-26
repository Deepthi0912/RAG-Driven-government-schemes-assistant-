from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    scheme_id = Column(
        Integer,
        ForeignKey("schemes.id"),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    processing_status = Column(
        String(50),
        default="pending"
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )