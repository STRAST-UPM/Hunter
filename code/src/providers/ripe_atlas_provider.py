# external imports
from time import sleep
import asyncio
import requests
import json

# internal imports
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.hunter_models.measurement_model import MeasurementModel
from ..data_models.hunter_models.base_measurement_result_model import BaseMeasurementResultModel
from ..data_models.hunter_models.traceroute_model import TracerouteModel
from ..data_models.hunter_models.traceroute_hop_model import TracerouteHopModel
from ..data_models.hunter_models.hop_response_model import HopResponseModel

from ..data_models.ripe_models.base_definition_ripe_measurement_request_model import BaseDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ripe_models.ripe_measurement_response_model import RipeMeasurementResponseModel

from ..utilities.logger import logger
from ..utilities.enums import (
    AddressFamilyRIPEMeasurementRequest,
    DefinitionTypeRIPEMeasurementRequest,
    MeasurementStatusRIPE
)
from ..utilities.constants import (
    RIPE_ATLAS_TIME_BETWEEN_RESULTS_REQUESTS_SECONDS,
    RIPE_ATLAS_MEASUREMENTS_URL,
    RIPE_ATLAS_MEASUREMENTS_RESULTS_URL,
    RIPE_ATLAS_PROBES_URL
)

class RIPEAtlasProvider:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def start_new_measurement(
            self,
            definitions: list[BaseDefinitionRIPEMeasurementRequestModel],
            probes: list[ProbeObjectRipeMeasurementRequestModel],
    ) -> RipeMeasurementResponseModel:
        try:
            logger.debug("Log from: RIPEAtlasProvider.start_new_measurement")
            logger.debug(f"Measurement definition: {definitions}")
            logger.debug(f"Measurement probes: {probes}")

            start_measurement_response = requests.post(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {self._api_key}",
                },
                json={
                    "definitions": [
                        definition.model_dump() for definition in definitions],
                    "probes": [
                        probe.model_dump() for probe in probes],
                },
            )

            logger.debug("Log from: RIPEAtlasProvider.start_new_measurement")
            logger.debug(json.dumps(start_measurement_response.json(), indent=4))

            if start_measurement_response.ok:
                measurement_response = RipeMeasurementResponseModel(
                    **start_measurement_response.json())
            else:
                logger.warning("Log from: RIPEAtlasProvider.start_new_measurement")
                logger.warning(start_measurement_response.json())

                errors_descriptions = [
                    error["detail"]
                    for error in start_measurement_response.json()["error"]["errors"]
                ]

                measurement_response = RipeMeasurementResponseModel(
                    error=True,
                    error_description=errors_descriptions.__str__()
                )
        except Exception as error:
            logger.error("Exception log from: RIPEAtlasProvider.start_new_measurement")
            logger.error(error)
            measurement_response = RipeMeasurementResponseModel(
                error=True,
                error_description="Error parsing the message"
            )

        return measurement_response

    def get_measurement_description(self, measurement_id: int) -> [MeasurementModel, None] :
        # TODO change for using a RIPEMeasurementDescriptionModel
        try:
            measurement_description_response = requests.get(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {self._api_key}",
                },
                params={
                    "id": measurement_id,
                }
            ).json()

            logger.debug("Log from: RIPEAtlasProvider.get_measurement_description")
            logger.debug(json.dumps(measurement_description_response, indent=4))

            measurement_description_result = measurement_description_response["results"][0]

            measurement = MeasurementModel(
                id=measurement_description_result["id"],
                timestamp=measurement_description_result["start_time"],
                address_family=AddressFamilyRIPEMeasurementRequest(
                    measurement_description_result["af"]),
                description=measurement_description_result["description"],
                is_oneoff=measurement_description_result["is_oneoff"],
                is_public=measurement_description_result["is_public"],
                resolve_on_probe=measurement_description_result["resolve_on_probe"],
                target=measurement_description_result["target"],
                target_ip=measurement_description_result["target_ip"],
                target_asn=measurement_description_result["target_asn"],
                type=DefinitionTypeRIPEMeasurementRequest(
                    measurement_description_result["type"]),
                results=[]
            )

            return measurement
        except Exception as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_description")
            logger.error(error)
            return None

    def get_measurement_status(self, measurement_id: int) -> MeasurementStatusRIPE:
        try:
            measurement_description_response = requests.get(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {self._api_key}",
                },
                params={
                    "id": measurement_id,
                }
            ).json()

            logger.debug("Log from: RIPEAtlasProvider.get_measurement_status")
            logger.debug(
                MeasurementStatusRIPE(
                    measurement_description_response["results"][0]["status"]["id"]
                )
            )

            return MeasurementStatusRIPE(
                measurement_description_response["results"][0]["status"]["id"]
            )

        except requests.HTTPError as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_status")
            logger.error(error)
            return MeasurementStatusRIPE.FAILED

    def get_measurement_expected_number_result(self, measurement_id: int) -> int:
        try:
            measurement_description_response = requests.get(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {self._api_key}",
                },
                params={
                    "id": measurement_id,
                }
            ).json()

            logger.debug("Log from: RIPEAtlasProvider.get_measurement_expected_number_result")
            logger.debug(f"Probes scheduled: {measurement_description_response["results"][0]["probes_scheduled"]}")

            return measurement_description_response["results"][0]["probes_scheduled"]

        except requests.HTTPError as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_expected_number_result")
            logger(error)
            return 0

    def get_measurement_type(self, measurement_id: int) -> [DefinitionTypeRIPEMeasurementRequest, None]:
        try:
            measurement_description_response = requests.get(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {self._api_key}",
                },
                params={
                    "id": measurement_id,
                }
            )

            measurement_type = DefinitionTypeRIPEMeasurementRequest(
                measurement_description_response.json()["results"][0]["type"]
            )

            logger.debug("Log from: RIPEAtlasProvider.get_measurement_type")
            logger.debug(f"Measurement type: {measurement_type}")

            return measurement_type

        except Exception as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_type")
            logger.error(error)
            return None

    async def get_measurement_results(
            self,
            measurement_id: int,
            measurement_type: DefinitionTypeRIPEMeasurementRequest) \
            -> [list[BaseMeasurementResultModel], None] :

        measurement_results_response = []
        try:
            # If measurement type is different fom the wanted one return None
            if measurement_type != self.get_measurement_type(measurement_id):
                return []

            enough_measurements = False
            measurement_not_ongoing = False

            while (not enough_measurements) or (not measurement_not_ongoing):
                logger.debug(
                    f"Waiting {RIPE_ATLAS_TIME_BETWEEN_RESULTS_REQUESTS_SECONDS}"
                    f" seconds for proper results of measurement {measurement_id}"
                )
                await asyncio.sleep(RIPE_ATLAS_TIME_BETWEEN_RESULTS_REQUESTS_SECONDS)

                measurement_results_response = requests.get(
                    url=RIPE_ATLAS_MEASUREMENTS_RESULTS_URL.format(
                        measurement_id=measurement_id
                    ),
                    headers={
                        "Authorization": f"Key {self._api_key}",
                    }
                ).json()

                enough_measurements = (
                        len(measurement_results_response) >=
                        self.get_measurement_expected_number_result(measurement_id))
                measurement_not_ongoing = (
                    (self.get_measurement_status(measurement_id) != MeasurementStatusRIPE.SPECIFIED) or
                    (self.get_measurement_status(measurement_id) != MeasurementStatusRIPE.SCHEDULED) or
                    (self.get_measurement_status(measurement_id) != MeasurementStatusRIPE.ONGOING)
                )

                logger.debug("Log from: RIPEAtlasProvider.get_measurement_results")
                logger.debug(f"Measurements length {len(measurement_results_response)}")

            match measurement_type:
                case DefinitionTypeRIPEMeasurementRequest.TRACEROUTE:
                    return self.parse_measurement_traceroute_result(measurement_results_response)
                case DefinitionTypeRIPEMeasurementRequest.PING:
                    return []
                case _:
                    return []

        except requests.HTTPError as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_results")
            logger.error(measurement_results_response)
            logger.error(error)
            return []

    def parse_measurement_traceroute_result(self, measurement_results: list[dict]) -> [TracerouteModel]:
        traceroute_results = []

        logger.debug("Log from: RIPEAtlasProvider.parse_measurement_traceroute_result")
        logger.debug(f"Number of results: {len(measurement_results)}")

        if len(measurement_results) == 0:
            return traceroute_results

        for traceroute_result in measurement_results:
            traceroute_results.append(
                TracerouteModel(
                    timestamp=traceroute_result["timestamp"],
                    probe_id=traceroute_result["prb_id"],
                    origin_ip=traceroute_result["src_addr"],
                    public_origin_ip=traceroute_result["from"],
                    destination_ip=traceroute_result["dst_addr"],
                    destination_name=traceroute_result["dst_name"],
                    hops=[TracerouteHopModel(
                        hop_position=traceroute_hop_result["hop"],
                        hop_responses= [HopResponseModel(
                            ip_address=hop_response["from"] if "from" in hop_response.keys() else "*",
                            ttl=hop_response["ttl"] if "ttl" in hop_response.keys() else 0,
                            rtt_ms=hop_response["rtt"] if "rtt" in hop_response.keys() else 0,
                        ) for hop_response in traceroute_hop_result["result"]],
                    ) for traceroute_hop_result in traceroute_result["result"]],
                )
            )

        return traceroute_results

    def get_probe_location_info(self, probe_id: int) -> (str, float, float):
        """
        :param probe_id: id of the probe we want the info
        :return: (country_code, latitude, longitude)
        """

        country_code = ""
        latitude = 0.0
        longitude = 0.0

        try:
            probe_info = requests.get(
                url=f"{RIPE_ATLAS_PROBES_URL}/{probe_id}"
            ).json()

            country_code = probe_info["country_code"]
            latitude = probe_info["geometry"]["coordinates"][1]
            longitude = probe_info["geometry"]["coordinates"][0]

        except Exception as e:
            logger.error("Exception log from: RIPEAtlasProvider.get_probe_location_info")
            logger.error(e)

        return country_code, latitude, longitude