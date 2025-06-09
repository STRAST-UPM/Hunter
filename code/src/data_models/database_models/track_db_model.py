# external imports
from sqlalchemy import Column, Integer

# internal imports
from .base_db_model import BaseDBModel

class TrackDBModel(BaseDBModel):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
