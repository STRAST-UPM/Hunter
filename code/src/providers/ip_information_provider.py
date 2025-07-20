# external imports
import json
import ipaddress
import requests
import ipinfo
from os import getenv

# internal imports
from ..utilities.logger import logger
from ..utilities.constants import (
    IPINFO_CACHE_IP_INFO
)


class IPInformationProvider:
    def __init__(self):
        self._ipinfo_api_key: str = getenv("IPINFO_TOKEN")

    def locate_unicast_ip(self, ip_address: str) -> [(str, str, float, float), None]:
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        """

        if self.is_bogon(ip_address):
            return None

        ip_location = self.locate_unicast_with_cached_ipinfo(
            ip_address=ip_address,
        )

        if ip_location is None:
            logger.debug("Log from: IPInformationProvider.locate_unicast_ip")
            logger.debug("Private IPInfo request needed")
            ip_location = self.locate_unicast_with_ipinfo(
                ip_address=ip_address,
            )

        return ip_location

    def locate_unicast_with_ipinfo(self, ip_address: str) -> [(str, str, float, float), None]:
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
                    return None
            except Exception as e:
                pass

            return details.country, details.city, details.latitude, details.longitude
        except Exception as e:
            logger.error("Exception log from: IPInformationProvider.locate_unicast_with_ipinfo")
            logger.error(e)
            return None

    def locate_unicast_with_cached_ipinfo(self, ip_address: str) -> [(str, str, float, float), None]:
        """

        :param ip_address: ip address to locate
        :return: (country_code: str, city_name: str, latitude: float, longitude: float)
        If an error occurs, return None
        """

        try:
            ip_address_details_str = requests.get(
                url=IPINFO_CACHE_IP_INFO.format(ip_address=ip_address),
            ).json()["details"]
            ip_address_details = json.loads(ip_address_details_str)

            if ("bogon" in ip_address_details.keys()) and (ip_address_details["bogon"]):
                return None

            return ip_address_details["country"], ip_address_details["city"], ip_address_details["latitude"], ip_address_details["longitude"]
        except Exception as e:
            logger.error("Exception log from: IPInformationProvider.locate_unicast_with_cached_ipinfo")
            logger.error(e)
            return None

    def is_anycast_service_check(self, ip_address: str) -> bool:
        # TODO
        return True

    def is_bogon(self, ip_address: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_address)
            return (ip.is_private or
                    ip.is_reserved or
                    ip.is_loopback or
                    ip.is_link_local or
                    ip.is_multicast or
                    ip.is_unspecified)
        except ValueError:
            return False
