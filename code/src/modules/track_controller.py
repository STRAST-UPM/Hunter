# external imports

# internal imports
from ..data_models.track_model import TrackModel
from ..data_models.ip_address_model import IpAddressModel
from ..utilities.enums import TrackStatus


class TrackController:
    def __init__(self):
        self._track: TrackModel = None


    def track_ip(
            self,
            ip_to_track: IpAddressModel
    ) -> bool:
        self._track = TrackModel(
            ip_to_track=ip_to_track,
            status=TrackStatus.IN_PROGRESS,
        )



        return True

# https://fastapi.tiangolo.com/tutorial/body/#declare-it-as-a-parameter