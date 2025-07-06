# external imports
from time import sleep
import requests
import json

# internal imports
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.hunter_models.measurement_model import MeasurementModel
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
            # print(json.dumps(start_measurement_response.json(), indent=4))

            if start_measurement_response.ok:
                measurement_response = RipeMeasurementResponseModel(
                    **start_measurement_response.json())
            else:
                measurement_response = RipeMeasurementResponseModel(
                    error=True
                )
        # TODO change errors for generals and print object
        except requests.HTTPError as error:
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

    def get_measurement_results(
            self,
            measurement_id: int,
            measurement_type: DefinitionTypeRIPEMeasurementRequest) -> [None] :
        try:
            measurement_results_response = requests.get(
                url=RIPE_ATLAS_MEASUREMENTS_RESULTS_URL.format(
                    measurement_id=measurement_id
                ),
                headers={
                    "Authorization": f"Key {self._api_key}",
                }
            ).json()

            sleep(10)
            print(self.get_measurement_expected_number_result(measurement_id))
            print(self.get_measurement_status(measurement_id))


            # LOG: response
            print(json.dumps(measurement_results_response, indent=4))

            # If measurement type is different fom the wanted one return None
            if measurement_type != "":
                return None

            match measurement_type:
                case DefinitionTypeRIPEMeasurementRequest.TRACEROUTE:
                    pass
                case DefinitionTypeRIPEMeasurementRequest.PING:
                    pass
                case _:
                    return None

        except requests.HTTPError as error:
            print(error)
            return None

    def parse_measurement_traceroute_result(self):
        pass
