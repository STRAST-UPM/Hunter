# external imports
from pydantic import BaseModel
from datetime import datetime

# internal imports
from .ip_address_model import IpAddressModel
from .measurement_model import MeasurementModel
from .track_result_model import TrackResultModel
from ...utilities.enums import TrackStatus


class TrackModel(BaseModel):
    id: int
    timestamp: datetime
    status: TrackStatus
    status_description: str
    slim: bool
    ip: IpAddressModel

    track_results: list[TrackResultModel]
    measurements: list[MeasurementModel]
