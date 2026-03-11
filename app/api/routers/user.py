from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register")
async def register_user():
    pass