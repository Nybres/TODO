from fastapi import APIRouter

from app.api.dependencies import TaskServiceDep, PaginationDep, UserServiceDep, UserDep
from app.api.schemas.task import TaskPageResponse, TaskCreateSchema, TaskReadSchema

router = APIRouter(
    prefix="/task",
    tags=["task"],
)

@router.get("/", response_model=TaskPageResponse)
async def get(
        service: TaskServiceDep,
        pagination: PaginationDep,
        current_user: UserDep,
):
    return await service.get_tasks(pagination, current_user)

@router.post("/", response_model=TaskReadSchema)
async def add(
        task: TaskCreateSchema,
        service: TaskServiceDep,
        current_user: UserDep,
):
    return await service.add(task, current_user)


async def update():
    pass


async def delete():
    pass