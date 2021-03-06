from fastapi import APIRouter
from routers.v1 import auth, users, source

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(source.router, tags=["source"])

