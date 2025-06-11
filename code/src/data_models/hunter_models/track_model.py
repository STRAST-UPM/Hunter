# external imports
from pydantic import BaseModel
from datetime import datetime

# internal imports
from .ip_address_model import IpAddressModel
from ...utilities.enums import TrackStatus
from .track_result_model import TrackResultModel


class TrackModel(BaseModel):
    id: int
    timestamp: datetime
    status: TrackStatus
    status_description: str
    slim: bool
    ip: IpAddressModel

    track_results: list[TrackResultModel]
