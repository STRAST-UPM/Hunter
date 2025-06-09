# external imports
from fastapi import FastAPI

# internal imports
## Routers imports
from src.routers import *
## Database imports
from src.providers.database_provider import DatabaseProvider
# Necesario para cargar los modelos y crear las tablas
from src.data_models.database_models import *

db_provider = DatabaseProvider()
db_provider.create_all()

# needs to be created outside __main__ to be found by the executing command
app = FastAPI()

# Routers inclusion
app.include_router(router=default_router)
app.include_router(router=track_router)
