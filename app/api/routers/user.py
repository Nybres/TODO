from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.api.dependencies import UserServiceDep, UserDep, PaginationDep
from app.api.schemas.user import UserCreateSchema, UserReadSchema, UserListSchema
from app.core.security import TokenData

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register", response_model=UserReadSchema)
async def register_user(user: UserCreateSchema, service: UserServiceDep):
    return await service.add(user)

@router.post("/login", response_model=TokenData)
async def login_user(
        request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: UserServiceDep,
):
   token = await service.login(
       request_form.username,
       request_form.password,
   )
   return {
       "access_token": token,
       "token_type": "jwt",
   }

@router.get('/logout')
async def logout_user():
    return {"message": "Logged out"}

@router.get('/users', response_model=UserListSchema)
async def get_users(
        service: UserServiceDep,
        pagination: PaginationDep,
        current_user: UserDep,
):
    return await service.get_users(pagination, current_user)