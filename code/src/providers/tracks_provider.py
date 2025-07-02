# external imports
from datetime import datetime

# internal imports
from .database_provider import DatabaseProvider
from .ip_address_provider import IPAddressProvider
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

    def create_new_track(
            self,
            ip_address: str,
            slim: bool,
            check_if_anycast: bool) -> TrackModel:

        ip_address_provider = IPAddressProvider()
        track_db_model = TrackDBModel(
            timestamp=datetime.now(),
            status=TrackStatus.IN_PROGRESS.value,
            status_description=TRACK_STATUS_IN_PROGRESS_DESCRIPTION,
            slim=slim,
            ip_address=ip_address
        )

        if ip_address_provider.is_address_in_db(ip_address):
            track_added = self.add(track_db_model)
        else:
            ip_address_provider.add_new_ip_address(
                ip_address=ip_address,
                check_if_anycast=check_if_anycast
            )
            track_added = self.add(track_db_model)

        return TrackModel.from_db(track_added)

    def mark_track_with_error(self, track_id: int):
        track_db = self.get_by_id(model_class=TrackDBModel, obj_id=track_id)
        track_db.status = TrackStatus.ERROR.value
        self.update(track_db)