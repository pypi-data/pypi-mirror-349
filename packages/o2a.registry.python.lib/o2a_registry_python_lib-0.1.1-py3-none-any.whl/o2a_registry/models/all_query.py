from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar("T")


class AllQuery(BaseModel, Generic[T]):
    offset: int
    hits: int
    totalHits: int
    records: List[T]
    duration: int
