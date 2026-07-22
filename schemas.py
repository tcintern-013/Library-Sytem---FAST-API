from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    id: int
    title: str
    author: str


class BookResponse(BookCreate):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)