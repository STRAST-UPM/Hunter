# external imports
from fastapi import APIRouter

# internal imports
from ..data_models.ip_address_model import IpAddressModel
from ..modules.track_controller import TrackController
from ..utilities.endpoints_tags import (
    TRACK_TAG,
    BASE_ENDPOINT,
    TRACK_IP_ENDPOINT
)

track_router = APIRouter(
    tags=[TRACK_TAG],
    prefix=BASE_ENDPOINT,
)
track_controller = TrackController()


@track_router.post(f"{TRACK_IP_ENDPOINT}/{{ip_address}}")
def get_track(ip_address: str) -> dict[str, bool]:
    ip_to_track = IpAddressModel(
        # TODO check ip address format
        address=ip_address,
        # TODO check if IP is anycast
        is_anycast=True,
        # TODO check if IP is bogon, not private
        is_bogon=False
    )

    return {"track_started": track_controller.track_ip(ip_to_track)}
