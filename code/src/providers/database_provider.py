# external imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# internal imports
from ..data_models.database_models.base_db_model import BaseDBModel
from ..utilities.constants import (
    DATABASE_URL
)


class DatabaseProvider:
    def __init__(self):
        self._engine = create_engine(
            url=DATABASE_URL,
            echo=True,
        )

        self._session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    def create_all(self):
        BaseDBModel.metadata.create_all(bind=self._engine, checkfirst=True)

    def drop_all(self):
        BaseDBModel.metadata.drop_all(bind=self._engine, checkfirst=True)
