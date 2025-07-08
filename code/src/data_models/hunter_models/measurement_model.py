# external imports
from typing import Optional, Type

from pydantic import BaseModel
from datetime import datetime

# internal imports
from .base_measurement_result_model import BaseMeasurementResultModel

from ...utilities.enums import (
    DefinitionTypeRIPEMeasurementRequest,
    AddressFamilyRIPEMeasurementRequest
)

class MeasurementModel(BaseModel):
    id: int
    timestamp: datetime
    address_family: AddressFamilyRIPEMeasurementRequest
    description: str
    is_oneoff: bool
    is_public: bool
    resolve_on_probe: bool
    target: str
    target_ip: str
    target_asn: Optional[int]
    type: DefinitionTypeRIPEMeasurementRequest

    results: list[Type[BaseMeasurementResultModel]]
