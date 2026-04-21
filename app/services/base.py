import math
from typing import Generic, TypeVar, Type, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pagination import PaginationParams

T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, id: int ):
        return await self.session.get(self.model, id)

    async def _add(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity):
        # return await self._add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _delete(self, entity):
        await self.session.delete(entity)

    def apply_sorting(self, query, sort_key: str, order: str):
        column = getattr(self.model, sort_key)

        if order == "desc":
            return query.order_by(column.desc())
        return query.order_by(column.asc())

    async def _get_paginated_result(self, query: Any, params: PaginationParams) -> dict:
        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await self.session.execute(count_query)
        total_count = total_count_result.scalar() or 0

        offset = (params.page - 1) * params.page_size
        paginated_query = query.offset(offset).limit(params.page_size)

        result = await self.session.execute(paginated_query)
        items = result.scalars().all()

        total_pages = math.ceil(total_count / params.page_size) if total_count > 0 else 0

        return {
            "items": items,
            "total": total_count,
            "page": params.page,
            "page_size": params.page_size,
            "total_pages": total_pages,
            "has_next": params.page < total_pages,
            "has_previous": params.page > 1
        }