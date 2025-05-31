from fastapi import APIRouter
from .v1 import users

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(users.router, tags=["users"])
