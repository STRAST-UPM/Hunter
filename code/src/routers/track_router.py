# external imports
from fastapi import APIRouter

# internal imports
from ..data_models.track_request_model import TrackRequestModel
from ..data_models.track_start_response_model import TrackStartReponseModel
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



@track_router.post(f"{TRACK_IP_ENDPOINT}")
async def post_track_ip(track_request: TrackRequestModel) -> TrackStartReponseModel:
    track_controller = TrackController()
    return await track_controller.post_track_ip(track_request)
