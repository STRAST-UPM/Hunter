# external imports
from dataclasses import dataclass

# internal imports
from ..utilities.enums import ProbeObjectTypeRIPEMeasurementRequest


@dataclass(kw_only=True)
class ProbeObjectRipeMeasurementRequestModel:
    requested: int
    type: ProbeObjectTypeRIPEMeasurementRequest
    value: [str, int]
