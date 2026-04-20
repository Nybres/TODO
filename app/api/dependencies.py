from typing import Annotated, Literal
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.core.security import oauth2_scheme_user
from app.database.models import User
from app.database.session import get_session
from app.services.tag import TagService
from app.services.task import TaskService
from app.services.user import UserService
from app.utils import decode_access_token
from fastapi import HTTPException, status

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return data

def get_pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order: Literal["asc", "desc"] = Query("asc")
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size, order=order)


PaginationDep = Annotated[PaginationParams, Depends(get_pagination_params)]


def get_user_service(session: SessionDep):
    return UserService(session)


def get_tag_service(session: SessionDep):
    return TagService(session)


def get_task_service(session: SessionDep):
    return TaskService(session)


async def get_user_access_token(
        token: Annotated[str, Depends(oauth2_scheme_user)],
) -> dict:
    return await _get_access_token(token)


async def get_current_user(
        token_data: Annotated[dict, Depends(get_user_access_token)],
        session: SessionDep
):
    user = await session.get(
        User,
        token_data["user"]["id"],
    )

    if user is None:
        raise ValueError("Invalid user")

    return user


UserDep = Annotated[User, Depends(get_current_user)]


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
TagServiceDep = Annotated[TagService, Depends(get_tag_service)]
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]