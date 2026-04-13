from typing import Annotated, Literal
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.database.session import get_session
from app.services.tag import TagService
from app.services.user import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

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






UserServiceDep = Annotated[UserService, Depends(get_user_service)]
TagServiceDep = Annotated[TagService, Depends(get_tag_service)]