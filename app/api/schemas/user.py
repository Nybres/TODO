from pydantic import BaseModel,EmailStr

from app.api.schemas.pagination import PaginatedResponse


class BaseUserSchema(BaseModel):
    name: str
    email: EmailStr

class UserCreateSchema(BaseUserSchema):
    password: str

class UserReadSchema(BaseUserSchema):
    id: int
    name: str
    email: str

class UserListSchema(PaginatedResponse[UserReadSchema]):
    pass
