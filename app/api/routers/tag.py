from fastapi import APIRouter, Depends

from app.api.dependencies import TagServiceDep, PaginationDep, get_current_user
from app.api.schemas.tag import TagPageResponse, TagCreateSchema, TagReadSchema

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/", response_model=TagPageResponse)
async def get_tags(
        service: TagServiceDep,
        pagination: PaginationDep
):
    return await service.get_tags_page(pagination)


@router.post("/", response_model=TagReadSchema)
async def create_tag(
        tag: TagCreateSchema,
        service: TagServiceDep
):
    return await service.add(tag)