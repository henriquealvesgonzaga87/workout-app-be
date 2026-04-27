from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TraningTypeInputDto(BaseModel):
    name: Optional[str | None] = None
    creation_date: Optional[datetime | None] = None
    update_date: Optional[datetime | None] = None


class TrainingTypeOutputDto(BaseModel):
    id: int
    name: str
    creation_date: datetime
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True
