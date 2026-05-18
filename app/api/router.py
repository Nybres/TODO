from fastapi import APIRouter
from .routers import user, tag, task, dashboard

master_router = APIRouter()

master_router.include_router(user.router)
master_router.include_router(tag.router)
master_router.include_router(task.router)

master_router.include_router(dashboard.router)