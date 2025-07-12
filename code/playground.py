# external imports
import json

import requests
import ipinfo
from os import getenv

# internal imports
from src .utilities.constants import (
    IPINFO_CACHE_IP_INFO
)


class IPInformationProvider:
    def __init__(self):
        self._ipinfo_api_key: str = getenv("IPINFO_TOKEN")

    def locate_unicast_ip(self, ip_address: str) -> (str, str, float, float):
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        """

        # TODO

        country_code = "country_code"
        city_name = "city_name"
        latitude = 0.0
        longitude = 0.0

        return country_code, city_name, latitude, longitude

    def locate_unicast_with_ipinfo(self, ip_address: str) -> (str, str, float, float):
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        If an error occurs, return ("", "", 0, 0)
        """

        try:
            handler = ipinfo.getHandler(self._ipinfo_api_key)
            details = handler.getDetails(ip_address)

            try:
                if details.bogon:
                    return "", "", 0, 0
            except Exception as e:
                pass

            return details.country, details.city, details.latitude, details.longitude
        except Exception as e:
            print("Exception from IPInformationProvider.locate_unicast_with_ipinfo")
            print(e)
            return "", "", 0, 0

    def locate_unicast_with_cached_ipinfo(self, ip_address: str) -> (str, str, float, float):
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        If an error occurs, return ("", "", 0, 0)
        """

        try:
            ip_address_details_str = requests.get(
                url=IPINFO_CACHE_IP_INFO.format(ip_address=ip_address),
            ).json()["details"]
            ip_address_details = json.loads(ip_address_details_str)

            if ("bogon" in ip_address_details.keys()) and (ip_address_details["bogon"]):
                return "", "", 0, 0

            return ip_address_details["country"], ip_address_details["city"], ip_address_details["latitude"], ip_address_details["longitude"]
        except Exception as e:
            print("Exception from IPInformationProvider.locate_unicast_with_cached_ipinfo")
            print(e)
            return "", "", 0, 0

ip_information_provider = IPInformationProvider()
values = ip_information_provider.locate_unicast_with_cached_ipinfo("88.54.65.123")
print(values)