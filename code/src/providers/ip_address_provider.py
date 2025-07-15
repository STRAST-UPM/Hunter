# external imports

# internal imports
from .database_provider import DatabaseProvider
from .ip_information_provider import IPInformationProvider
from ..data_models.hunter_models.ip_address_model import IpAddressModel
from ..data_models.database_models import IpAddressDBModel


class IPAddressProvider(DatabaseProvider):
    def __init__(self):
        super().__init__()
        self._ip_information_provider = IPInformationProvider()

    def add_new_ip_address(
            self,
            ip_address: str,
            check_if_anycast: bool = False,) -> IpAddressModel:

        return IpAddressModel.from_db(self.add(
            IpAddressDBModel(
                address=ip_address,
                is_bogon=self._ip_information_provider.is_bogon(ip_address),
                is_anycast= self._ip_information_provider.
                is_anycast_service_check(ip_address) if check_if_anycast else True,
            )
        ))

    def is_address_in_db(self, ip_address: str) -> bool:
        return self.exists(
            model_class=IpAddressDBModel,
            obj_id=ip_address
        )
