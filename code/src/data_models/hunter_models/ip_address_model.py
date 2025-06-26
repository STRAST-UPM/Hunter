# external imports
from pydantic import BaseModel

# internal imports
from ..database_models import IpAddressDBModel


class IpAddressModel(BaseModel):
    address: str
    is_anycast: bool
    is_bogon: bool

    @classmethod
    def from_db(cls, ip_address_db_model: IpAddressDBModel) -> "IpAddressModel":
        return cls(
            address=ip_address_db_model.address,
            is_anycast=ip_address_db_model.is_anycast,
            is_bogon=ip_address_db_model.is_bogon,
        )
