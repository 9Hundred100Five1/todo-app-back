from fastapi import APIRouter

from app.api.endpoints import items, signin, users, signup

api_router = APIRouter()
api_router.include_router(signin.router, tags=["signin"])
api_router.include_router(signup.router, tags=["signup"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])