# external imports
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

# internal imports
from .base_db_model import BaseDBModel


class IpAddressDBModel(BaseDBModel):
    __tablename__ = "ip_addresses"

    address = Column(String, primary_key=True)
    is_anycast = Column(Boolean, nullable=False)
    is_bogon = Column(Boolean, nullable=False)

    # Relationships
    tracks = relationship("TrackDBModel", back_populates="ip_address_obj")
