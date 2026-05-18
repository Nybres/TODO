from fastapi import APIRouter

from app.api.dependencies import TaskServiceDep, UserDep
from app.api.schemas.dashboard import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("/", response_model=DashboardResponse)
async def get(
        service: TaskServiceDep,
        current_user: UserDep,
        limit: int = 5,
):
    return await service.get_dashboard(current_user, limit)