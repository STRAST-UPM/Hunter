# external imports
import uvicorn
from fastapi import FastAPI

# internal imports
from src.routers import *
from src.providers.database_provider import DatabaseProvider
from src.data_models.database_models import *
from src.utilities.constants import HUNTER_PORT


db_provider = DatabaseProvider()
db_provider.create_all()

# needs to be created outside __main__ to be found by the executing command
app = FastAPI()

# Routers inclusion
app.include_router(router=default_router)
app.include_router(router=track_router)
