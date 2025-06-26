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

    track_results: Optional[list[TrackResultModel]] = None
    measurements: Optional[list[MeasurementModel]] = None

    @classmethod
    def from_db(cls, track_db_model: TrackDBModel) -> "TrackModel":
        return cls(
            id=track_db_model.id,
            timestamp=track_db_model.timestamp,
            status=TrackStatus(track_db_model.status),
            status_description=track_db_model.status_description,
            slim=track_db_model.slim,
            ip_address=track_db_model.ip_address,
        )
