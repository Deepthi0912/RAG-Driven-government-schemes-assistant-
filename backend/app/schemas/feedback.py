
from pydantic import BaseModel, Field
from typing import Literal, Optional


class FeedbackCreate(BaseModel):
    query_id: int
    rating: Literal["helpful", "not_helpful"]
    comment: Optional[str] = Field(
        default=None,
        max_length=1000
    )


class FeedbackResponse(BaseModel):
    id: int
    query_id: int
    user_id: int
    rating: str
    comment: Optional[str] = None

    class Config:
        from_attributes = True
