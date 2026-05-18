from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from app.api.schemas.pagination import PaginatedResponse


class BaseTag(BaseModel):
    name: str

class TagCreateSchema(BaseTag):
    pass

class TagReadSchema(BaseTag):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TagPageResponse(PaginatedResponse[TagReadSchema]):
    top_priority_tag: str | None = None