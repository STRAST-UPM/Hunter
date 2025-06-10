# external imports
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class PingDBModel(BaseDBModel):
    __tablename__ = "pings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    probe_id = Column(Integer, nullable=False)
    origin_ip = Column(String, nullable=False)
    public_origin_ip = Column(String, nullable=False)
    destination_name = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    max_rtt_ms = Column(Float, nullable=False)
    min_rtt_ms = Column(Float, nullable=False)
    average_rtt_ms = Column(Float, nullable=False)
    caverage_area_polygon = Column(String, nullable=True)
    measurement_id = Column(Integer, ForeignKey('measurements.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    measurement = relationship("MeasurementDBModel", back_populates="pings")
