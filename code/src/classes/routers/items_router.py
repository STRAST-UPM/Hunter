# external imports
from fastapi import APIRouter

# internal imports
from ...utilities.endpoints_tags import (
    ITEMS_TAG,
    BASE_ITEMS_ENDPOINT
)

items_router = APIRouter(
    prefix=BASE_ITEMS_ENDPOINT,
    tags=[ITEMS_TAG],
)

@items_router.get("/list")
async def get_items_list():
    return ["Item1", "Item2", "Item3", "Item4", "Item5"]
