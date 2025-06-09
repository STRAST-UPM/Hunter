# external imports
from pydantic import BaseModel

# internal imports
from ...utilities.enums import ProbeObjectTypeRIPEMeasurementRequest


class ProbeObjectRipeMeasurementRequestModel(BaseModel):
    requested: int
    type: ProbeObjectTypeRIPEMeasurementRequest
    value: str
