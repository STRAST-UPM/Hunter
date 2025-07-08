# external imports
from pydantic import BaseModel

# internal imports

class HopResponseModel(BaseModel):
    ip_address: str
    ttl: int
    rtt_ms: float
