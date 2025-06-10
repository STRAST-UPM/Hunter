# external imports
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class TracerouteHopDBModel(BaseDBModel):
    __tablename__ = "traceroutes_hops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hop_position = Column(Integer, nullable=False)
    traceroute_id = Column(Integer, ForeignKey('traceroutes.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    traceroute = relationship("TracerouteDBModel", back_populates="traceroutes_hops")
    hops_responses = relationship("HopResponseDBModel", back_populates="hop")
