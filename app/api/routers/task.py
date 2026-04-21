from fastapi import APIRouter

from app.api.dependencies import TaskServiceDep, PaginationDep, UserServiceDep, UserDep
from app.api.schemas.task import TaskPageResponse, TaskCreateSchema, TaskReadSchema, TaskUpdateSchema

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


@router.patch('/{task_id}', response_model=TaskReadSchema)
async def update(
        task_id: int,
        task_data: TaskUpdateSchema,
        service: TaskServiceDep,
        current_user: UserDep,
):
    return await service.update(task_id, task_data, current_user)


@router.delete('/{task_id}')
async def delete(
        task_id: int,
        service: TaskServiceDep,
        current_user: UserDep,
):
    await service.delete(task_id, current_user)