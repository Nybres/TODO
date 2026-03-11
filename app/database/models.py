from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects import postgresql
from pydantic import EmailStr
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
            onupdate=datetime.now
        )
    )
