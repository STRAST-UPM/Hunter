# external imports
from pydantic import BaseModel

# internal imports

class HopResponseModel(BaseModel):
    id: int
    ip_address: str
    ttl: int
    rtt_ms: float
