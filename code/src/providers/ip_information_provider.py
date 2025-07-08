# external imports
import requests

# internal imports


class IPInformationProvider:
    def __init__(self):
        pass

    def locate_unicast_ip(self, ip_address: str) -> (str, str, float, float):
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        """

        country_code = "country_code"
        city_name = "city_name"
        latitude = 0.0
        longitude = 0.0

        return country_code, city_name, latitude, longitude