from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, mongo_item, redis_item, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(mongo_item.router, prefix="/mongo_item", tags=["mongo_item"])
api_router.include_router(redis_item.router, prefix="/redis_item", tags=["redis_item"])
