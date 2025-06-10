# external imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class TrackDiscIntersectionAirportDBModel(BaseDBModel):
    __tablename__ = "track_disc_intersections_airports"

    track_result_intersection_area_id = Column(Integer, ForeignKey('tracks_results.id', ondelete='CASCADE'), primary_key=True)
    airport_iata_code = Column(String, ForeignKey('airports.iata_code', ondelete='CASCADE'), primary_key=True)

    # Relationships
    track_result = relationship("TrackResultDBModel", back_populates="track_disc_intersections")
    airport = relationship("AirportDBModel", back_populates="track_disc_intersections")
