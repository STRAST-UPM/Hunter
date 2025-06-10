# external imports

# internal imports
from .database_provider import DatabaseProvider
from ..data_models.hunter_models.track_model import TrackModel
from ..data_models.database_models import TrackDBModel
from ..utilities.enums import (
    TrackStatus
)
from ..utilities.constants import (
    TRACK_STATUS_IN_PROGRESS_DESCRIPTION
)


class TracksProvider(DatabaseProvider):
    def __init__(self):
        super().__init__()

    def create_new_track(self):
        return self.add(
            db_model=TrackDBModel(
                status=TrackStatus.IN_PROGRESS.value,
                status_description=TRACK_STATUS_IN_PROGRESS_DESCRIPTION,
            ),
        )
