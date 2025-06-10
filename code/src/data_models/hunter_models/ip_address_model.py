# external imports
from pydantic import BaseModel

# internal imports


class IpAddressModel(BaseModel):
    address: str
    is_anycast: bool
    is_bogon: bool
