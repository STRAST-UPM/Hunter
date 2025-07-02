# external imports
import requests
import json

# internal imports
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.ripe_models.base_definition_ripe_measurement_request_model import BaseDefinitionRIPEMeasurementRequestModel
from ..data_models.ripe_models.probe_object_ripe_measurement_request_model import ProbeObjectRipeMeasurementRequestModel
from ..data_models.ripe_models.ripe_measurement_response_model import RipeMeasurementResponseModel
from ..utilities.constants import (
    RIPE_ATLAS_MEASUREMENTS_URL
)

class RIPEAtlasProvider:
    def __init__(self):
        pass

    def start_new_measurement(
            self,
            definitions: list[BaseDefinitionRIPEMeasurementRequestModel],
            probes: list[ProbeObjectRipeMeasurementRequestModel],
            ripe_api_key: str,
    ) -> RipeMeasurementResponseModel:
        try:
            # LOG: measurement parameters
            print(definitions)
            print(probes)

            start_measurement_response = requests.post(
                url=RIPE_ATLAS_MEASUREMENTS_URL,
                headers={
                    "Authorization": f"Key {ripe_api_key}",
                },
                json={
                    "definitions": [
                        definition.model_dump() for definition in definitions],
                    "probes": [
                        probe.model_dump() for probe in probes],
                },
            )

            # LOG: response
            print(json.dumps(start_measurement_response.json(), indent=4))

            if start_measurement_response.ok:
                measurement_response = RipeMeasurementResponseModel(
                    **start_measurement_response.json())
            else:
                measurement_response = RipeMeasurementResponseModel(
                    error=True
                )

        except requests.HTTPError as error:
            print(error)
            measurement_response = RipeMeasurementResponseModel(
                error=True,
            )

        return measurement_response

    def get_measurement_results(self):
        pass
