# external imports
from fastapi import APIRouter

# internal imports
from ..utilities.endpoints_tags import (
    DEFAULT_TAG,
    DEFAULT_ENDPOINT
)

default_router = APIRouter(
    tags=[DEFAULT_TAG]
)

@default_router.get(DEFAULT_ENDPOINT)
async def root():
    return "Hello World!"
