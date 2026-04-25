from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.api.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskShareSchema, TaskUpdateSharedSchema
from app.database.models import Task, User, TaskTag, SharedTask, Tag
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

    async def _get_shared_task(self, task_id: int, user_id: int) -> Task:
        task = await self.session.scalar(
            select(Task)
            .join(SharedTask, SharedTask.task_id == Task.id)
            .where(
                Task.id == task_id,
                SharedTask.shared_with_user_id == user_id,
                Task.deleted_at.is_(None)
            )
        )

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return task


    async def get_shared_task(self, task_id: int, current_user: User) -> Task:
        return await self._get_shared_task(task_id, current_user.id)


    async def get_shared_with_me(self, pagination: PaginationParams, current_user: User) -> dict:
        query = (
            select(Task)
            .join(SharedTask, SharedTask.task_id == Task.id)
            .where(
                SharedTask.shared_with_user_id == current_user.id,
                Task.deleted_at.is_(None)
            )
        )
        return await self._get_paginated_result(query, pagination)


    async def get_tasks(self, pagination: PaginationParams, current_user: User) -> dict:
        query = select(self.model).where(self.model.user_id == current_user.id)
        paginated_data = await self._get_paginated_result(query, pagination)
        return paginated_data


    async def get_task(self, task_id: int, current_user: User) -> Task:
        return await self._get_user_task(task_id, current_user.id)


    async def add(self, task: TaskCreateSchema, current_user: User) -> Task:
        new_task = Task(
            **task.model_dump(exclude={"tag_ids"}),
            user_id = current_user.id
        )

        await self._add(new_task)

        for tag_id in task.tag_ids:
            tag = await self.session.get(Tag, tag_id)
            if tag is None:
                raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
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
                tag = await self.session.get(Tag, tag_id)
                if tag is None:
                    raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
                self.session.add(TaskTag(task_id=task.id, tag_id=tag_id))

        return await self._update(task)


    async def delete(self, task_id: int, current_user: User) -> None:
        task = await self._get_user_task(task_id, current_user.id)
        task.deleted_at = datetime.now()
        await self._update(task)


    async def share(self, task_id: int, current_user: User, shared_with_user_id: int) -> None:
        if shared_with_user_id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot share task with yourself")

        task = await self._get_user_task(task_id, current_user.id)
        user = await self.session.get(User, shared_with_user_id)


        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        existing = await self.session.scalar(
            select(SharedTask).where(
                SharedTask.task_id == task_id,
                SharedTask.shared_with_user_id == shared_with_user_id,
            )
        )

        if existing:
            raise HTTPException(status_code=400, detail="Task already shared with this user")


        shared_task = SharedTask(task_id=task_id, shared_with_user_id=shared_with_user_id)
        await self._add(shared_task)


    async def unshare(self, task_id: int, current_user: User, shared_with_user_id: int) -> None:
        await self._get_user_task(task_id, current_user.id)

        shared = await self.session.scalar(
            select(SharedTask).where(
                SharedTask.task_id == task_id,
                SharedTask.shared_with_user_id == shared_with_user_id,
            )
        )

        if shared is None:
            raise HTTPException(status_code=404, detail="Task not shared with this user")

        await self._delete(shared)
        await self.session.commit()


    async def update_shared_task(self, task_id: int, task_data: TaskUpdateSharedSchema, current_user: User) -> Task:
        task = await self._get_shared_task(task_id, current_user.id)
        task.status = task_data.status
        return await self._update(task)