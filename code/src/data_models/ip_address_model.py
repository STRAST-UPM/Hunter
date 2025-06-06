# external imports
from dataclasses import dataclass

# internal imports

@dataclass
class IpAddressModel:
    address: str
    is_anycast: bool
    is_bogon: bool
