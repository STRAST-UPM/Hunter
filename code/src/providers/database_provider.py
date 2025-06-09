# external imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Type, List, Optional

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

        self._session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    @contextmanager
    def get_session(self) -> Session:
        session = self._session_local()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add(self, db_model: BaseDBModel):
        with self.get_session() as session:
            session.add(db_model)
            session.flush()
            return db_model.id

    def get_by_id(self, db_model: BaseDBModel, obj_id) -> BaseDBModel | None:
        with self.get_session() as session:
            return session.query(db_model).get(obj_id)

    def get_all(self, db_model: BaseDBModel) -> list[BaseDBModel]:
        with self.get_session() as session:
            return session.query(db_model).all()

    def delete(self, db_model: BaseDBModel):
        with self.get_session() as session:
            session.delete(db_model)

    def create_all(self):
        BaseDBModel.metadata.create_all(bind=self._engine, checkfirst=True)

    def drop_all(self):
        BaseDBModel.metadata.drop_all(bind=self._engine, checkfirst=True)
