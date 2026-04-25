from sqlmodel import SQLModel, Field, Column, Relationship, Enum as SAEnum
from enum import Enum
from sqlalchemy.dialects import postgresql
from pydantic import EmailStr
from datetime import datetime
from typing import Optional, List


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)


class SharedTask(SQLModel, table=True):
    __tablename__ = "shared_tasks"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    shared_with_user_id: int = Field(foreign_key="user.id", primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)

    created_at: datetime = Field(sa_column=Column(postgresql.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    tasks: List["Task"] = Relationship(back_populates="owner")
    shared_tasks: List["Task"] = Relationship(
        back_populates="shared_with",
        link_model=SharedTask,
        sa_relationship_kwargs = {"lazy": "selectin"}
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(
        sa_column=Column(SAEnum(TaskStatus, name="task_status"), default=TaskStatus.todo)
    )
    priority: TaskPriority = Field(
        sa_column=Column(SAEnum(TaskPriority, name="task_priority"), default=TaskPriority.medium)
    )

    due_date: Optional[datetime] = None
    created_at: datetime = Field(sa_column=Column(postgresql.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )
    deleted_at: Optional[datetime] = None

    owner: User = Relationship(back_populates="tasks")

    tags: List[Tag] = Relationship(
        link_model=TaskTag,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    shared_with: List[User] = Relationship(
        back_populates="shared_tasks",
        link_model=SharedTask,
        sa_relationship_kwargs={"lazy": "selectin"}
    )