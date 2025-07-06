# external imports
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel

from ..hunter_models.measurement_model import MeasurementModel


class MeasurementDBModel(BaseDBModel):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    address_family = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    is_oneoff = Column(Boolean, nullable=False)
    is_public = Column(Boolean, nullable=False)
    resolve_on_probe = Column(Boolean, nullable=False)
    target = Column(String, nullable=False)
    target_ip = Column(String, nullable=False)
    target_asn = Column(Integer, nullable=True)
    type = Column(String, nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    track = relationship("TrackDBModel", back_populates="measurements")
    traceroutes = relationship("TracerouteDBModel", back_populates="measurement")
    pings = relationship("PingDBModel", back_populates="measurement")
