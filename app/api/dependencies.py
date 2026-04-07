from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.user import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep):
    return UserService(session)








UserServiceDep = Annotated[UserService, Depends(get_user_service)]