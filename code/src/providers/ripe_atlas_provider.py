# external imports
import requests
import json

# internal imports
from ..data_models.ip_address_model import IpAddressModel

class RIPEAtlasProvider:
    def __init__(self, api_key: str):
        self._api_key = api_key


    def start_measurement(
            self,
            definitions: list,
            probes: list,
    ):
        pass

        try:
            start_measurment_response = requests.post(
                url="",
                json=""
            ).json()
        except requests.HTTPError as error:
            print(error)
