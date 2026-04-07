from passlib.exc import PasswordValueError
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from app.api.schemas.user import UserCreateSchema
from app.services.base import BaseService
from app.database.models import User

from sqlalchemy import select

from fastapi import HTTPException, status

from app.utils import generate_access_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
        self.model = User
        self.session = session


    async def add(self, user: UserCreateSchema) -> User:
        return await self._add_user(user.model_dump())

    async def login(self, email: str, password: str) -> str:
        return await self._generate_token(email, password)

    async def _add_user(self, data: dict) -> User:
        try:
            user = self.model(
                **data,
                password_hash=password_context.hash(data['password'])
            )
        except PasswordValueError:
            raise ValueError("Invalid password")

        created_user = await self._add(user)
        return created_user

    async def _get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email: str, password: str) -> str:
        user = await self._get_by_email(email)

        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return generate_access_token(
            data={
                "user":{
                    "name": user.name,
                    "id": user.id
                }
            }
        )