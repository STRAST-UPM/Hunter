# external imports
import asyncio

# internal imports
from ..data_models.track_model import TrackModel
from ..data_models.track_request_model import TrackRequestModel
from ..data_models.track_start_response_model import TrackStartReponseModel
from ..data_models.ripe_models.traceroute_definition_ripe_measurement_request_model import TracerouteDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ip_address_model import IpAddressModel
from ..utilities.enums import (
    TrackStatus,
    AddressFamilyRIPEMeasurementRequest
)
from ..utilities.constants import (
    TRACEROUTE_MEASUREMENT_DESCRIPTION
)


class TrackController:
    def __init__(self):
        pass


    async def post_track_ip(self, track_request: TrackRequestModel) -> TrackStartReponseModel:
        asyncio.create_task(self.track_ip(track_request))

        return TrackStartReponseModel(track_id=0)

    async def track_ip(self, track_request: TrackRequestModel):
        self.traceroute_track_phase(track_request=track_request)

        if not track_request.slim_method:
            self.ping_track_phase(track_request=track_request)

        await asyncio.sleep(20)

        print("hola!!!!!!!!!!!!!!!!!!!!!")


    def traceroute_track_phase(self, track_request: TrackRequestModel):
        traceroute_definition = TracerouteDefinitionRIPEMeasurementRequestModel(
            description=TRACEROUTE_MEASUREMENT_DESCRIPTION,
            af=AddressFamilyRIPEMeasurementRequest.IPV4,
            target=track_request.ip_address,
        )

        traceroutes_probes = ProbeObjectRipeMeasurementRequestModel(
            requested=track_request.probes_requested,
            type=track_request.probes_selection_type,
            value=track_request.probes_values,
        )

    def ping_track_phase(self, track_request: TrackRequestModel):
        pass
