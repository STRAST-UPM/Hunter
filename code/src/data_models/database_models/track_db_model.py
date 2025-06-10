# external imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class TrackDBModel(BaseDBModel):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    status_description = Column(String, nullable=False)
    slim = Column(Boolean, nullable=False)
    ip_address = Column(String, ForeignKey('ip_addresses.address', ondelete='CASCADE'), nullable=False)

    # Relationships
    ip_address_obj = relationship("IpAddressDBModel", back_populates="tracks")
    tracks_results = relationship("TrackResultDBModel", back_populates="track")
    measurements = relationship("MeasurementDBModel", back_populates="track")
