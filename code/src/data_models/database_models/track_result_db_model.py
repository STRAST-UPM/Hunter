# external imports
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class TrackResultDBModel(BaseDBModel):
    __tablename__ = "tracks_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_country = Column(String, nullable=True)
    origin_latitude = Column(Float, nullable=True)
    origin_longitude = Column(Float, nullable=True)
    destination_country = Column(String, nullable=True)
    destination_city = Column(String, nullable=True)
    destination_latitude = Column(Float, nullable=True)
    destination_longitude = Column(Float, nullable=True)
    intersection_area_polygon = Column(String, nullable=True)
    track_id = Column(Integer, ForeignKey('tracks.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    track = relationship("TrackDBModel", back_populates="tracks_results")
    track_disc_intersections = relationship("TrackDiscIntersectionAirportDBModel", back_populates="track_result")
