# external imports
from dataclasses import dataclass

# internal imports
from .ip_address_model import IpAddressModel
from ..utilities.enums import TrackStatus


@dataclass
class TrackModel:
    ip_to_track: IpAddressModel
    status: TrackStatus
