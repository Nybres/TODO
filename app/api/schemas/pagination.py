from typing import TypeVar, Generic, List, Literal
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    order: Literal["asc", "desc"] = "asc"

class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
