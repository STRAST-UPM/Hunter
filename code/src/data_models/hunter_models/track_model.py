# external imports
from typing import Optional

from pydantic import BaseModel
from datetime import datetime

# internal imports
from .measurement_model import MeasurementModel
from .track_result_model import TrackResultModel
from ..database_models import TrackDBModel
from ...utilities.enums import TrackStatus


class TrackModel(BaseModel):
    id: int
    timestamp: datetime
    status: TrackStatus
    status_description: str
    slim: bool
    ip_address: str

    track_results: list[TrackResultModel]
    measurements: list[MeasurementModel]
