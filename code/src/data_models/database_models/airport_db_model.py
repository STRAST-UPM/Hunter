# external imports
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class AirportDBModel(BaseDBModel):
    __tablename__ = "airports"

    iata_code = Column(String, primary_key=True)
    size = Column(String, nullable=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country_code = Column(String, nullable=False)
    city_name = Column(String, nullable=False)

    # Relationships
    track_disc_intersections = relationship("TrackDiscIntersectionAirportDBModel", back_populates="airport")
