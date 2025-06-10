# external imports
from pydantic import BaseModel

# internal imports
from ..utilities.enums import ProbeObjectTypeRIPEMeasurementRequest


class TrackRequestModel(BaseModel):
    ip_address: str
    check_if_anycast: bool = False
    slim: bool = True
    probes_requested: int
    probes_selection_type: ProbeObjectTypeRIPEMeasurementRequest
    probes_values: str
    api_key: str = None
