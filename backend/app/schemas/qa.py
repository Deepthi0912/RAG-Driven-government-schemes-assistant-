from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Question about an Indian government scheme"
    )


class SourceReference(BaseModel):
    source_file: str
    page_number: int | str

class AskResponse(BaseModel):
    query_id: int
    answer: str
    sources: list[SourceReference]
    timings: dict[str, float]