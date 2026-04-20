from datetime import datetime

from pydantic import BaseModel

from app.api.schemas.pagination import PaginatedResponse
from app.api.schemas.tag import TagReadSchema
from app.database.models import TaskStatus, TaskPriority


class BaseTask(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: datetime | None = None


class TaskCreateSchema(BaseTask):
    tag_ids: list[int] = []


class TaskReadSchema(BaseTask):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagReadSchema] = []


class TaskPageResponse(PaginatedResponse[TaskReadSchema]):
    pass