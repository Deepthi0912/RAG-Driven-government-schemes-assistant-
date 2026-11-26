from pydantic import BaseModel


class SchemeCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    ministry: str | None = None
    official_url: str | None = None


class SchemeResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: str | None = None
    ministry: str | None = None
    official_url: str | None = None

    class Config:
        from_attributes = True