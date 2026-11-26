
from datetime import datetime
from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    sources: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True
