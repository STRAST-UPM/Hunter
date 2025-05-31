# external imports
from fastapi import APIRouter

# internal imports
from ...utilities.endpoints_tags import (
    USERS_TAG,
    BASE_USERS_ENDPOINT
)

users_router = APIRouter(
    prefix=BASE_USERS_ENDPOINT,
    tags=[USERS_TAG]
)

@users_router.get("/list")
async def get_users_list():
    return ["User1", "User2"]

@users_router.get("/first")
async def get_users_first():
    return "User1"
