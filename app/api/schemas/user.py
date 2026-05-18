from pydantic import BaseModel, EmailStr, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)

class UserListSchema(PaginatedResponse[UserReadSchema]):
    pass
