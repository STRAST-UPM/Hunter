# external imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Type, List, Optional, TypeVar, Generic
import logging

# internal imports
from ..data_models.database_models.base_db_model import BaseDBModel
from ..utilities.constants import DATABASE_URL

# Type variable for better type hinting
T = TypeVar('T', bound=BaseDBModel)

logger = logging.getLogger(__name__)


class DatabaseProvider:
    def __init__(self):
        self._engine = create_engine(
            url=DATABASE_URL,
            # change to False in production
            echo=False,
            # check connections before using them
            pool_pre_ping=True,
            # recycle connections every hour
            pool_recycle=3600,
        )

        self._session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager for safe session handling.
        """
        session = self._session_local()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()

    def add(self, db_model: BaseDBModel) -> Optional[int]:
        """
        Adds a new object to the database.

        Args:
            db_model: Model instance to add

        Returns:
            ID of the created object or None if it fails
        """
        try:
            with self.get_session() as session:
                session.add(db_model)
                # Get the generated ID
                session.flush()
                # Refresh the object with database data
                session.refresh(db_model)
                return db_model.id
        except SQLAlchemyError as e:
            logger.error(f"Error adding object: {e}")
            return None

    def get_by_id(self, model_class: Type[T], obj_id) -> Optional[T]:
        """
        Gets an object by its ID.

        Args:
            model_class: Model class (not instance)
            obj_id: ID of the object to search

        Returns:
            Found object or None
        """
        try:
            with self.get_session() as session:
                obj = session.query(model_class).get(obj_id)
                if obj:
                    # Prevent detached object issues
                    session.expunge(obj)
                return obj
        except SQLAlchemyError as e:
            logger.error(f"Error getting object by ID {obj_id}: {e}")
            return None

    def get_all(self, model_class: Type[T]) -> List[T]:
        """
        Gets all objects of a model.

        Args:
            model_class: Model class

        Returns:
            List of objects
        """
        try:
            with self.get_session() as session:
                objects = session.query(model_class).all()
                # Expunge objects to make them usable outside session
                for obj in objects:
                    session.expunge(obj)
                return objects
        except SQLAlchemyError as e:
            logger.error(f"Error getting all objects: {e}")
            return []

    def update(self, db_model: BaseDBModel) -> bool:
        """
        Updates an existing object.

        Args:
            db_model: Model instance to update

        Returns:
            True if updated successfully, False otherwise
        """
        try:
            with self.get_session() as session:
                session.merge(db_model)
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating object: {e}")
            return False

    def delete_by_id(self, model_class: Type[T], obj_id) -> bool:
        """
        Deletes an object by its ID.

        Args:
            model_class: Model class
            obj_id: ID of the object to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            with self.get_session() as session:
                obj = session.query(model_class).get(obj_id)
                if obj:
                    session.delete(obj)
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting object with ID {obj_id}: {e}")
            return False

    def delete(self, db_model: BaseDBModel) -> bool:
        """
        Deletes a specific object.

        Args:
            db_model: Model instance to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            with self.get_session() as session:
                # Merge first in case the object is detached
                merged_obj = session.merge(db_model)
                session.delete(merged_obj)
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting object: {e}")
            return False

    def exists(self, model_class: Type[T], obj_id) -> bool:
        """
        Checks if an object with the given ID exists.

        Args:
            model_class: Model class
            obj_id: ID to check

        Returns:
            True if exists, False otherwise
        """
        try:
            with self.get_session() as session:
                return session.query(model_class).filter(
                    model_class.id == obj_id
                ).first() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence of ID {obj_id}: {e}")
            return False

    def count(self, model_class: Type[T]) -> int:
        """
        Counts the total number of records for a model.

        Args:
            model_class: Model class

        Returns:
            Number of records
        """
        try:
            with self.get_session() as session:
                return session.query(model_class).count()
        except SQLAlchemyError as e:
            logger.error(f"Error counting objects: {e}")
            return 0

    def create_all(self) -> bool:
        """
        Creates all tables defined in the models.

        Returns:
            True if created successfully, False otherwise
        """
        try:
            BaseDBModel.metadata.create_all(bind=self._engine, checkfirst=True)
            logger.info("Database tables created successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error creating tables: {e}")
            return False

    def drop_all(self) -> bool:
        """
        Drops all tables.

        Returns:
            True if dropped successfully, False otherwise
        """
        try:
            BaseDBModel.metadata.drop_all(bind=self._engine, checkfirst=True)
            logger.info("Database tables dropped successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error dropping tables: {e}")
            return False

    def close(self):
        """
        Closes the database engine.
        """
        if self._engine:
            self._engine.dispose()
            logger.info("Database engine disposed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()