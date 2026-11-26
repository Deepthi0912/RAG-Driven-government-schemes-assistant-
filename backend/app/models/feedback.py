from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    query_id = Column(
        Integer,
        ForeignKey("query_history.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    rating = Column(
        String(20),
        nullable=False
    )

    comment = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )