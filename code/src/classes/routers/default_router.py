# external imports
from fastapi import APIRouter

# internal imports
from ...utilities.endpoints_tags import (
    DEFAULT_TAG,
    BASE_ENDPOINT
)

default_router = APIRouter(
    tags=[DEFAULT_TAG]
)

@default_router.get("/")
async def root():
    return "Hello World!"
