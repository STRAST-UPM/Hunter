# external imports
import asyncio

# internal imports
from ..data_models.api_models.track_request_model import TrackRequestModel
from ..data_models.api_models.track_start_response_model import TrackStartResponseModel

from ..providers.tracks_provider import TracksProvider

from .hunter import Hunter


class TrackRequestsManager:
    def __init__(self):
        self._tracks_provider = TracksProvider()

    # API request controller handlers
    async def post_track_ip(self, track_request: TrackRequestModel) -> TrackStartResponseModel:
        track = self._tracks_provider.create_new_track(
            ip_address=track_request.ip_address,
            slim=track_request.slim,
            check_if_anycast=track_request.check_if_anycast,
        )

        hunter = Hunter(
            track=track,
            api_key=track_request.api_key,
            probes_requested=track_request.probes_requested,
            probes_values=track_request.probes_values,
            probes_selection_type=track_request.probes_selection_type,
        )
        asyncio.create_task(hunter.track_ip())

        return TrackStartResponseModel(track_id=track.id)
