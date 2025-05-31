# external imports
from fastapi import FastAPI

# internal imports
# Routers imports
from src.classes.routers import *

# needs to be created outside __main__ to be found by the executing command
app = FastAPI()

# Routers inclusion
app.include_router(router=default_router)
app.include_router(router=users_router)
app.include_router(router=items_router)
