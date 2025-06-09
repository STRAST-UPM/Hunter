# external imports
from sqlalchemy import Column, Integer, String

# internal imports
from .base_db_model import BaseDBModel


class TrackDBModel(BaseDBModel):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Integer, nullable=False)
    status_description = Column(String, nullable=False)
