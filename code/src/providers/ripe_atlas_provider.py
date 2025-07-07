# external imports
from time import sleep
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
from ..utilities.enums import (
    AddressFamilyRIPEMeasurementRequest,
    DefinitionTypeRIPEMeasurementRequest,
    MeasurementStatusRIPE
)
from ..utilities.constants import (
    RIPE_ATLAS_MEASUREMENTS_URL,
    RIPE_ATLAS_MEASUREMENTS_RESULTS_URL,
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
            # LOG: measurement parameters
            # print(f"Log of parameters from: RIPEAtlasProvider.start_new_measurement")
            # print(definitions)
            # print(probes)

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

            # LOG: response
            # print("Log response from: RIPEAtlasProvider.start_new_measurement")
            # print(json.dumps(start_measurement_response.json(), indent=4))

            if start_measurement_response.ok:
                measurement_response = RipeMeasurementResponseModel(
                    **start_measurement_response.json())
            else:
                # LOG: error response
                print("Log reponse error from: RIPEAtlasProvider.start_new_measurement")
                print(start_measurement_response.json())
                measurement_response = RipeMeasurementResponseModel(
                    error=True
                )
        # TODO change errors for generals and print object
        except Exception as error:
            # LOG: general exception
            print("Log exception from: RIPEAtlasProvider.start_new_measurement")
            print(error)
            measurement_response = RipeMeasurementResponseModel(
                error=True,
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

            # LOG: response
            # print(json.dumps(measurement_description_response, indent=4))

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
            )

            return measurement
        except requests.HTTPError as error:
            print(error)
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

            # LOG: responseresponse
            # print(json.dumps(measurement_description_response, indent=4))
            # print(
            #     MeasurementStatusRIPE(
            #         measurement_description_response["results"][0]["status"]["id"]
            #     )
            # )

            return MeasurementStatusRIPE(
                measurement_description_response["results"][0]["status"]["id"]
            )

        except requests.HTTPError as error:
            print(error)
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

            # LOG: response
            # print(json.dumps(measurement_description_response, indent=4))
            # print(
            #     MeasurementStatusRIPE(
            #         measurement_description_response["results"][0]["probes_scheduled"]
            #     )
            # )

            return measurement_description_response["results"][0]["probes_scheduled"]

        except requests.HTTPError as error:
            print(error)
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
            ).json()

            # LOG: response
            # print(json.dumps(measurement_description_response, indent=4))
            # print(
            #     MeasurementStatusRIPE(
            #         measurement_description_response["results"][0]["probes_scheduled"]
            #     )
            # )

            return DefinitionTypeRIPEMeasurementRequest(
                measurement_description_response["results"][0]["type"]
            )

        except Exception as error:
            print(error)
            return None

    def get_measurement_results(
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
                print("Waiting 30 seconds for proper results...")
                sleep(30)

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

                # LOG: response
                print("Response log of get_measurements_results")
                print(json.dumps(measurement_results_response, indent=4))

            match measurement_type:
                case DefinitionTypeRIPEMeasurementRequest.TRACEROUTE:
                    return self.parse_measurement_traceroute_result(measurement_results_response)
                case DefinitionTypeRIPEMeasurementRequest.PING:
                    return []
                case _:
                    return []

        except requests.HTTPError as error:
            print("Error log from: RIPEAtlasProvider.get_measurement_results")
            print(measurement_results_response)
            print(error)
            return []

    def parse_measurement_traceroute_result(self, measurement_results: list[dict]) -> [TracerouteModel]:
        traceroute_results = []

        # LOG: results retrieved
        print(f"Number of results: {len(measurement_results)}")
        print(json.dumps(measurement_results, indent=4))

        if len(measurement_results) == 0:
            return traceroute_results

        # Here we put id of the traceroute results as 0, but the db has a Serial
        # should be updated
        for traceroute_result in measurement_results:
            traceroute_results.append(
                TracerouteModel(
                    id=0,
                    timestamp=traceroute_result["timestamp"],
                    probe_id=traceroute_result["prb_id"],
                    origin_ip=traceroute_result["src_addr"],
                    public_origin_ip=traceroute_result["from"],
                    destination_ip=traceroute_result["dst_addr"],
                    destination_name=traceroute_result["dst_name"],
                    hops=[TracerouteHopModel(
                        id=0,
                        hop_position=traceroute_hop_result["hop"],
                        hop_responses= [HopResponseModel(
                            id=0,
                            ip_address=hop_response["from"] if "from" in hop_response.keys() else "*",
                            ttl=hop_response["ttl"] if "ttl" in hop_response.keys() else 0,
                            rtt_ms=hop_response["rtt"] if "rtt" in hop_response.keys() else 0,
                        ) for hop_response in traceroute_hop_result["result"]],
                    ) for traceroute_hop_result in traceroute_result["result"]],
                )
            )

        return traceroute_results
