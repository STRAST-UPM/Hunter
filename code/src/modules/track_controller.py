# external imports
import asyncio
import json

# internal imports
from ..data_models.hunter_models.track_model import TrackModel
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.track_request_model import TrackRequestModel
from ..data_models.track_start_response_model import TrackStartReponseModel

from ..data_models.ripe_models.traceroute_definition_ripe_measurement_request_model import TracerouteDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ripe_models.ripe_measurement_response_model import RipeMeasurementResponseModel

from ..providers.tracks_provider import TracksProvider
from ..providers.ripe_atlas_provider import RIPEAtlasProvider

from ..utilities.enums import (
    TrackStatus,
    AddressFamilyRIPEMeasurementRequest
)
from ..utilities.constants import (
    TRACEROUTE_MEASUREMENT_DESCRIPTION
)


class TrackController:
    def __init__(self):
        self._tracks_provider = TracksProvider()
        self._ripe_atlas_provider = RIPEAtlasProvider()


    async def post_track_ip(self, track_request: TrackRequestModel) -> TrackStartReponseModel:
        asyncio.create_task(self.track_ip(track_request))

        track_id = self._tracks_provider.create_new_track(
            track_request=track_request)

        return TrackStartReponseModel(track_id=track_id)


    async def track_ip(self, track_request: TrackRequestModel):
        traceroute_measurement_response = self.traceroute_track_phase_start_measurement(track_request=track_request)

        print(json.dumps(traceroute_measurement_response.model_dump(), indent=4))

        if traceroute_measurement_response.error_msg is None:
            # TODO update track with error
            pass

        if not track_request.slim:
            self.ping_track_phase(track_request=track_request)


    def traceroute_track_phase_start_measurement(self, track_request: TrackRequestModel) -> RipeMeasurementResponseModel:
        traceroute_definition = TracerouteDefinitionRIPEMeasurementRequestModel(
            description=TRACEROUTE_MEASUREMENT_DESCRIPTION,
            target=track_request.ip_address,
        )

        traceroute_probes = ProbeObjectRipeMeasurementRequestModel(
            requested=track_request.probes_requested,
            type=track_request.probes_selection_type,
            value=track_request.probes_values,
        )

        return self._ripe_atlas_provider.start_new_measurement(
            definitions=[traceroute_definition],
            probes=[traceroute_probes],
            ripe_api_key=track_request.api_key,
        )


    def traceroute_track_phase_measurement_analysis(self, traceroute_measurement_id: int):
        pass

    def ping_track_phase(self, track_request: TrackRequestModel):
        pass
