from fastapi import APIRouter

from app.api.dependencies import TaskServiceDep, PaginationDep, UserServiceDep, UserDep
from app.api.schemas.task import TaskPageResponse, TaskCreateSchema, TaskReadSchema, TaskUpdateSchema, TaskShareSchema, \
    TaskUpdateSharedSchema

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

@router.get("/{task_id}", response_model=TaskReadSchema)
async def get_by_id(
        task_id: int,
        service: TaskServiceDep,
        current_user: UserDep,
):
    return await service.get_task(task_id, current_user)


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


@router.post('/{task_id}/share', status_code=204)
async def share(
        task_id: int,
        service: TaskServiceDep,
        current_user: UserDep,
        data: TaskShareSchema,
):
    await service.share(task_id, current_user, data.shared_with_user_id)


@router.delete('/{task_id}/share', status_code=204)
async def unshare(
        task_id: int,
        service: TaskServiceDep,
        current_user: UserDep,
        data: TaskShareSchema,
):
    await service.unshare(task_id, current_user, data.shared_with_user_id)


@router.get('shared-with-me', response_model=TaskPageResponse)
async def get_shared_with_me(
        service: TaskServiceDep,
        pagination: PaginationDep,
        current_user: UserDep,
):
    return await service.get_shared_with_me(pagination, current_user)


@router.get('shared-with-me/{task_id}', response_model=TaskReadSchema)
async def get_shared_task(
        task_id: int,
        service: TaskServiceDep,
        current_user: UserDep,
):
    return await service.get_shared_task(task_id, current_user)


@router.patch('shared-with-me/{task_id}', response_model=TaskReadSchema)
async def update_shared_task(
        task_id: int,
        task_data: TaskUpdateSharedSchema,
        service: TaskServiceDep,
        current_user: UserDep,
):
    return await service.update_shared_task(task_id, task_data, current_user)