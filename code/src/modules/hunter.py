# external imports

# internal imports
from ..data_models.hunter_models.track_model import TrackModel
from ..data_models.hunter_models.measurement_model import MeasurementModel
from ..data_models.hunter_models.traceroute_model import TracerouteModel
from ..data_models.hunter_models.track_result_model import TrackResultModel

from ..data_models.ripe_models.traceroute_definition_ripe_measurement_request_model import \
    TracerouteDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ripe_models.ripe_measurement_response_model import RipeMeasurementResponseModel

from ..providers.ripe_atlas_provider import RIPEAtlasProvider
from ..providers.tracks_provider import TracksProvider
from ..providers.measurements_provider import MeasurementsProvider
from ..providers.ip_information_provider import IPInformationProvider

from ..utilities.logger import logger
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
        self._ip_information_provider: IPInformationProvider = IPInformationProvider()

    async def track_ip(self):
        # Obtain the measurements
        traceroute_start_measurement_response = self._start_traceroute_measurement()

        if traceroute_start_measurement_response.error:
            self._tracks_provider.mark_track_with_error(
                track_id=self._track.id,
                error_msg=traceroute_start_measurement_response.error_description,
            )
            return

        self._save_measurements_description(
            measurement_ids=traceroute_start_measurement_response.measurement
        )

        await self._store_traceroute_measurement_results(
            measurement_ids=traceroute_start_measurement_response.measurement
        )

        self._update_track_with_all_data()

        logger.debug("Log from: Hunter.track_ip")
        logger.debug("Track with all relationships")
        logger.debug(self._track)

        if not self._track.slim:
            # TODO make ping phase
            pass

        # Compute the measurements with Hunter algorithm
        track_results: list[TrackResultModel] = []
        for measurement in self._track.measurements:
            if measurement.type != DefinitionTypeRIPEMeasurementRequest.TRACEROUTE:
                continue
            for traceroute in measurement.results:
                # TODO resolve warning
                partial_track_results = self._compute_traceroute_result(traceroute)
                if partial_track_results is not None:
                    track_results.extend(partial_track_results)

        # Save all track results
        for track_result in track_results:
            self._tracks_provider.save_track_result(
                track_result=track_result,
                track_id=self._track.id,
            )

        # Mark as finished the hunt
        self._tracks_provider.mark_track_as_finished(track_id=self._track.id)

    def _start_traceroute_measurement(self) -> RipeMeasurementResponseModel:
        traceroute_definition = TracerouteDefinitionRIPEMeasurementRequestModel(
            description=TRACEROUTE_MEASUREMENT_DESCRIPTION,
            target=self._track.ip_address,
        )

        traceroute_probes = []
        for probe_value in self._probes_values:
            traceroute_probes.append(ProbeObjectRipeMeasurementRequestModel(
                requested=self._probes_requested,
                type=self._probes_selection_type,
                value=probe_value,
            ))

        return self._ripe_atlas_provider.start_new_measurement(
            definitions=[traceroute_definition],
            probes=traceroute_probes,
        )

    def _save_measurements_description(self, measurement_ids: list[int]):
        for measurement_id in measurement_ids:
            measurement: MeasurementModel = self._ripe_atlas_provider.get_measurement_description(measurement_id)
            if measurement:
                measurement_saved = self._measurements_provider.save_measurement(
                    measurement_model=measurement,
                    track_id=self._track.id
                )

    async def _store_traceroute_measurement_results(self, measurement_ids: list[int]):
        for measurement_id in measurement_ids:
            traceroute_results = await self._get_traceroute_measurement_results(
                measurement_id=measurement_id
            )
            self._save_traceroute_results(
                traceroute_results=traceroute_results,
                measurement_id=measurement_id
            )

    async def _get_traceroute_measurement_results(self, measurement_id: int) -> list[TracerouteModel]:
            traceroute_results = await self._ripe_atlas_provider.get_measurement_results(
                measurement_id=measurement_id,
                measurement_type=DefinitionTypeRIPEMeasurementRequest.TRACEROUTE
            )

            logger.debug("Log from: Hunter._get_traceroute_measurement_results")
            logger.debug(traceroute_results)

            return traceroute_results

    def _save_traceroute_results(
            self,
            traceroute_results: list[TracerouteModel],
            measurement_id: int
    ):
        for traceroute_result in traceroute_results:
            self._measurements_provider.save_traceroute_results(
                traceroute_result=traceroute_result,
                measurement_id=measurement_id
            )

        logger.debug("Log from: Hunter._save_traceroute_results")
        logger.debug("Traceroute results saved in DB")

    def _update_track_with_all_data(self):
        self._track = self._tracks_provider.get_track_with_relations(
            track_id=self._track.id,
        )

    def _start_ping_measurement(self):
        # TODO
        pass

    def _get_ping_measurement_results(self):
        # TODO
        pass

    def _compute_traceroute_result(self, traceroute: TracerouteModel) -> list[TrackResultModel]:
        if not self._is_target_hop_valid(traceroute):
            logger.debug("Log from: Hunter._compute_traceroute_result")
            logger.debug(f"Target hop is not valid in track {self._track.id}")
            return []

        if not self._is_last_hop_valid(traceroute):
            logger.debug("Log from: Hunter._compute_traceroute_result")
            logger.debug(f"Last hop is not valid in track {self._track.id}")
            return []

        try:
            last_hop_responses = traceroute.hops[-2].hop_responses
        except IndexError as e:
            logger.debug("Exception log from: Hunter._compute_traceroute_result")
            logger.debug(e)
            return []

        probe_country_code, probe_latitude, probe_longitude = (
            self._ripe_atlas_provider.get_probe_location_info(traceroute.probe_id)
        )

        last_hop_ips = set([
            hop_response.ip_address
            for hop_response in last_hop_responses
            if hop_response.ip_address != "*"
        ])

        logger.debug("Log from: Hunter._compute_traceroute_result")
        logger.debug(f"IPs in last hop: {last_hop_ips}")

        track_results = []

        for ip_address in last_hop_ips:
            (last_hop_ip_country_code, last_hop_ip_city_name,
             last_hop_ip_latitude, last_hop_ip_longitude) = (
                self._ip_information_provider.locate_unicast_ip(ip_address)
            )

            track_results.append(
                TrackResultModel(
                    origin_country = probe_country_code,
                    origin_latitude = probe_latitude,
                    origin_longitude = probe_longitude,
                    destination_country = last_hop_ip_country_code,
                    destination_city = last_hop_ip_city_name,
                    destination_latitude = last_hop_ip_latitude,
                    destination_longitude = last_hop_ip_longitude,
                    intersection_area_polygon ="",
                    airports_in_intersection=[],
                )
            )

        return track_results

    def _is_target_hop_valid(self, traceroute_result: TracerouteModel) -> bool:
        try:
            target_hop_responses = traceroute_result.hops[-1].hop_responses
        except IndexError as e:
            logger.error("Exception log from: Hunter._compute_traceroute_result")
            logger.error(e)
            return False

        target_hop_ips = set([
            hop_response.ip_address
            for hop_response in target_hop_responses
            if hop_response.ip_address != "*"
        ])

        # Check if target hop ips are all the same
        if len(target_hop_ips) == 1:
            return True

        return False

    def _is_last_hop_valid(self, traceroute_result: TracerouteModel):
        try:
            last_hop_responses = traceroute_result.hops[-1].hop_responses
        except IndexError as e:
            logger.error("Exception log from: Hunter._compute_traceroute_result")
            logger.error(e)
            return False

        last_hop_ips = set([
            hop_response.ip_address
            for hop_response in last_hop_responses
            if hop_response.ip_address != "*"
        ])

        # Check if there are some clear IPs in last hop
        if len(last_hop_ips) > 0:
            return True

        return False