from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.api.schemas.task import TaskCreateSchema, TaskUpdateSchema
from app.database.models import Task, User, TaskTag
from app.services.base import BaseService


class TaskService(BaseService[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
        self.model = Task
        self.session = session

    async def _get_user_task(self, task_id: int, user_id: int) -> Task:
        task = await self.session.scalar(
            select(self.model).where(
                self.model.id == task_id,
                self.model.user_id == user_id,
                self.model.deleted_at.is_(None)
            )
        )

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    async def get_tasks(self, pagination: PaginationParams, current_user: User) -> dict:
        query = select(self.model).where(self.model.user_id == current_user.id)
        paginated_data = await self._get_paginated_result(query, pagination)
        return paginated_data

    async def add(self, task: TaskCreateSchema, current_user: User) -> Task:
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

    async def update(self, task_id: int, task_data: TaskUpdateSchema, current_user: User) -> Task:
        task = await self._get_user_task(task_id, current_user.id)
        update_data = task_data.model_dump(exclude_none=True, exclude={"tag_ids"})

        if not update_data and task_data.tag_ids is None:
            raise HTTPException(status_code=400, detail="No data to update")

        for field, value in update_data.items():
            setattr(task, field, value)

        if task_data.tag_ids is not None:
            old_tags = await self.session.scalars(
                select(TaskTag).where(TaskTag.task_id == task_id)
            )
            for tag in old_tags:
                await self.session.delete(tag)

            for tag_id in task_data.tag_ids:
                self.session.add(TaskTag(task_id=task.id, tag_id=tag_id))

        return await self._update(task)


    async def delete(self, task_id: int, current_user: User) -> None:
        task = await self._get_user_task(task_id, current_user.id)
        task.deleted_at = datetime.now()
        await self._update(task)