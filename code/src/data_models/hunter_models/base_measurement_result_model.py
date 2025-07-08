# external imports
from pydantic import BaseModel
from datetime import datetime

# internal imports

class BaseMeasurementResultModel(BaseModel):
    timestamp: datetime
    probe_id: int
    origin_ip: str
    public_origin_ip: str
