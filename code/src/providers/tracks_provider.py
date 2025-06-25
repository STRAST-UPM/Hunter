# external imports
from datetime import datetime

# internal imports
from .database_provider import DatabaseProvider
from .ip_address_provider import IPAddressProvider
from ..data_models.track_request_model import TrackRequestModel
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

    def create_new_track(self, track_request: TrackRequestModel):
        ip_address_provider = IPAddressProvider()
        track_db_model = TrackDBModel(
            timestamp=datetime.now(),
            status=TrackStatus.IN_PROGRESS.value,
            status_description=TRACK_STATUS_IN_PROGRESS_DESCRIPTION,
            slim=track_request.slim,
            ip_address=track_request.ip_address
        )

        if ip_address_provider.is_address_in_db(track_request.ip_address):
            track_id_added = self.add(track_db_model)
        else:
            ip_address_provider.add_new_ip(
                ip_address=track_request.ip_address
            )
            track_id_added = self.add(track_db_model)

        return
