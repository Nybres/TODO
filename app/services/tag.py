from sqlalchemy import select, func,desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams
from app.api.schemas.tag import TagCreateSchema
from app.database.models import Tag, TaskTag
from app.services.base import BaseService

from fastapi import  HTTPException, status


class TagService(BaseService[Tag]):
    def __init__(self, session: AsyncSession):
        super().__init__(Tag, session)
        self.model = Tag
        self.session = session

    async def get_tags_page(self, pagination: PaginationParams) -> dict:
        query = select(self.model)

        query = self.apply_sorting(query, "name", pagination.order)
        paginated_data = await self._get_paginated_result(query, pagination)

        most_popular_tag_query = (
            select(self.model.name)
            .join(TaskTag, isouter=True)
            .group_by(self.model.id)
            .order_by(desc(func.count(TaskTag.task_id)))
            .limit(1)
        )
        most_popular_result = await self.session.execute(most_popular_tag_query)

        paginated_data["top_priority_tag"] = most_popular_result.scalar_one_or_none()

        return paginated_data

    async def add(self, tag: TagCreateSchema) -> Tag:
        existing_tag = await self.session.scalar(
            select(self.model).where(self.model.name == tag.name)
        )

        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tag z nazwą '{tag.name}' już istnieje."
            )

        new_tag = Tag(
            **tag.model_dump(),
        )
        return await self._add(new_tag)
