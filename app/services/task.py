from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.api.schemas.task import TaskCreateSchema
from app.database.models import Task, User, TaskTag
from app.services.base import BaseService


class TaskService(BaseService[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
        self.model = Task
        self.session = session

    async def get_tasks(self, pagination: PaginationParams, current_user: User) -> dict:
        query = select(self.model).where(self.model.user_id == current_user.id)
        paginated_data = await self._get_paginated_result(query, pagination)
        return paginated_data

    async def add(self, task: TaskCreateSchema, current_user: User):
        new_task = Task(
            **task.model_dump(),
            user_id = current_user.id
        )

        await self._add(new_task)

        for tag_id in task.tag_ids:
            self.session.add(TaskTag(task_id=new_task.id, tag_id=tag_id))

        await self.session.commit()
        await self.session.refresh(new_task)

        return new_task

    async def update(self):
        pass


    async def delete(self):
        pass