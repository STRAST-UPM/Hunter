# external imports
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class HopResponseDBModel(BaseDBModel):
    __tablename__ = "hops_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    ttl = Column(Integer, nullable=False)
    rtt_ms = Column(Float, nullable=False)
    hop_id = Column(Integer, ForeignKey('traceroutes_hops.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    hop = relationship("TracerouteHopDBModel", back_populates="hops_responses")
