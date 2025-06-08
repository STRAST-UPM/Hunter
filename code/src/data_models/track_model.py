# external imports
from pydantic import BaseModel

# internal imports
from .ip_address_model import IpAddressModel
from ..utilities.enums import TrackStatus


class TrackModel(BaseModel):
    ip_to_track: IpAddressModel
    status: TrackStatus
