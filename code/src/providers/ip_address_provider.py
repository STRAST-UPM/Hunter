# external imports
from datetime import datetime
import ipaddress
from tabnanny import check

# internal imports
from .database_provider import DatabaseProvider
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.database_models import IpAddressDBModel


class IPAddressProvider(DatabaseProvider):
    def __init__(self):
        super().__init__()

    def add_new_ip_address(
            self,
            ip_address: str,
            check_if_anycast: bool = False,) -> IpAddressModel:

        return IpAddressModel.from_db(self.add(
            IpAddressDBModel(
                address=ip_address,
                is_bogon=self.check_is_bogon(ip_address),
                is_anycast= self.is_anycast_service_check(ip_address) if check_if_anycast else True,
            )
        ))

    def is_anycast_service_check(self, ip_address: str) -> bool:
        # TODO
        return True

    def check_is_bogon(self, ip_address: str) -> bool:
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

    def is_address_in_db(self, ip_address: str) -> bool:
        return self.exists(
            model_class=IpAddressDBModel,
            obj_id=ip_address
        )
