from fastapi import APIRouter
from ..services.user_service import get_users, get_user, create_user, update_user, delete_user

router = APIRouter()

@router.get("/users")
async def read_users():
    return await get_users()

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    return await get_user(user_id)

@router.post("/users")
async def create_user_route(user_data: dict):
    return await create_user(user_data)

@router.put("/users/{user_id}")
async def update_user_route(user_id: int, user_data: dict):
    return await update_user(user_id, user_data)

@router.delete("/users/{user_id}")
async def delete_user_route(user_id: int):
    return await delete_user(user_id)