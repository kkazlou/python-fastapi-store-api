from pydantic import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .schemas import ItemSummary, StoreSummary, TagSummary


class StoreCreate(BaseModel):
    name: str


class ItemCreate(BaseModel):
    name: str


class TagCreate(BaseModel):
    name: str


class StoreSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ItemSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StoreRead(BaseModel):
    id: int
    name: str
    items: List[ItemSummary] = []

    class Config:
        from_attributes = True


class ItemRead(BaseModel):
    id: int
    name: str
    stores: List[StoreSummary] = []
    tags: List[TagSummary] = []

    class Config:
        from_attributes = True


class TagRead(BaseModel):
    id: int
    name: str
    items: List[ItemSummary] = []

    class Config:
        from_attributes = True