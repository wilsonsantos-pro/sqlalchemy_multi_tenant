from typing import Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: Optional[str]


class ItemUpdate(BaseModel):
    pass
