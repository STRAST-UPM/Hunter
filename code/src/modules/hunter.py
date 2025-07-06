# external imports
import asyncio
import json

# internal imports
from ..data_models.hunter_models.track_model import TrackModel
from ..data_models.hunter_models.measurement_model import MeasurementModel

from ..data_models.ripe_models.traceroute_definition_ripe_measurement_request_model import \
    TracerouteDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ripe_models.ripe_measurement_response_model import RipeMeasurementResponseModel

from ..providers.ripe_atlas_provider import RIPEAtlasProvider
from ..providers.tracks_provider import TracksProvider
from ..providers.measurements_provider import MeasurementsProvider

from ..utilities.enums import (
    ProbeObjectTypeRIPEMeasurementRequest,
    DefinitionTypeRIPEMeasurementRequest
)
from ..utilities.constants import (
    TRACEROUTE_MEASUREMENT_DESCRIPTION
)


class Hunter:
    def __init__(
            self,
            track: TrackModel,
            api_key: str,
            probes_requested: int,
            probes_selection_type: ProbeObjectTypeRIPEMeasurementRequest,
            probes_values: list[str],
    ):
        self._track: TrackModel = track
        self._api_key: str = api_key
        self._probes_requested: int = probes_requested
        self._probes_selection_type: ProbeObjectTypeRIPEMeasurementRequest = probes_selection_type
        self._probes_values: list[str] = probes_values

        self._ripe_atlas_provider: RIPEAtlasProvider = RIPEAtlasProvider(api_key)
        self._tracks_provider: TracksProvider = TracksProvider()
        self._measurements_provider: MeasurementsProvider = MeasurementsProvider()

    async def track_ip(self):
        traceroute_start_measurement_response = self._start_traceroute_measurement()

        if traceroute_start_measurement_response.error:
            self._tracks_provider.mark_track_with_error(track_id=self._track.id)
            return

        self._save_measurements_description(
            measurement_ids=traceroute_start_measurement_response.measurement
        )

        self._get_traceroute_measurement_results(
            measurement_ids=traceroute_start_measurement_response.measurement
        )

        # TODO
        # Save the measurement data in DB
        ## MeasurementProvider / MeasurementModel add from_db
        # Function to get results of the measurement
        ## Times control and how to wait or not
        # Save traceroute measurements
        ## Save in DB
        ## Keep them in TracerouteModel to run the algorithm

        if not self._track.slim:
            # TODO make ping phase
            pass

    def _start_traceroute_measurement(self) -> RipeMeasurementResponseModel:
        traceroute_definition = TracerouteDefinitionRIPEMeasurementRequestModel(
            description=TRACEROUTE_MEASUREMENT_DESCRIPTION,
            target=self._track.ip_address,
        )

        traceroute_probes = None
        for probe_value in self._probes_values:
            traceroute_probes = ProbeObjectRipeMeasurementRequestModel(
                requested=self._probes_requested,
                type=self._probes_selection_type,
                value=probe_value,
            )

        return self._ripe_atlas_provider.start_new_measurement(
            definitions=[traceroute_definition],
            probes=[traceroute_probes],
        )

    def _get_traceroute_measurement_results(self, measurement_ids: list[int]):
        for measurement_id in measurement_ids:
            self._ripe_atlas_provider.get_measurement_results(
                measurement_id=measurement_id,
                measurement_type=DefinitionTypeRIPEMeasurementRequest.TRACEROUTE
            )

    def _start_ping_measurement(self):
        # TODO
        pass

    def _get_ping_measurement_results(self):
        # TODO
        pass

    def _save_measurements_description(self, measurement_ids: list[int]):
        for measurement_id in measurement_ids:
            measurement: MeasurementModel = self._ripe_atlas_provider.get_measurement_description(measurement_id)
            if measurement:
                measurement_saved = self._measurements_provider.save_measurement(
                    measurement_model=measurement,
                    track_id=self._track.id
                )
