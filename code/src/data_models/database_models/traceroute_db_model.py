# external imports
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class TracerouteDBModel(BaseDBModel):
    __tablename__ = "traceroutes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    probe_id = Column(Integer, nullable=False)
    origin_ip = Column(String, nullable=False)
    public_origin_ip = Column(String, nullable=False)
    destination_name = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    measurement_id = Column(Integer, ForeignKey('measurements.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    measurement = relationship("MeasurementDBModel", back_populates="traceroutes")
    traceroutes_hops = relationship("TracerouteHopDBModel", back_populates="traceroute")
