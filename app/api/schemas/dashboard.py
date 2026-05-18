from pydantic import BaseModel

from app.api.schemas.task import TaskReadSchema


class DashboardStats(BaseModel):
    total: int
    completed: int
    overdue: int


class DashboardResponse(BaseModel):
    recent_tasks: list[TaskReadSchema]
    stats: DashboardStats