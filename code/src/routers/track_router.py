# external imports
from fastapi import APIRouter

# internal imports
from ..data_models.api_models.track_request_model import TrackRequestModel
from ..data_models.api_models.track_start_response_model import TrackStartResponseModel
from ..modules.track_request_manager import TrackRequestsManager
from ..utilities.endpoints import (
    TRACK_TAG,
    BASE_ENDPOINT,
    BASE_TRACK_ENDPOINT,
    TRACK_IP_ENDPOINT
)

track_router = APIRouter(
    tags=[TRACK_TAG],
    prefix=BASE_ENDPOINT,
)


@track_router.post(f"{TRACK_IP_ENDPOINT}")
async def post_track_ip(track_request: TrackRequestModel) -> TrackStartResponseModel:
    track_request_manager = TrackRequestsManager()
    return await track_request_manager.post_track_ip(track_request)

@track_router.get(f"{BASE_TRACK_ENDPOINT}/"+"{track_id}", response_model_exclude_none=True)
def get_track_data(track_id: int):
    track_request_manager = TrackRequestsManager()
    return track_request_manager.get_track_data(track_id=track_id)