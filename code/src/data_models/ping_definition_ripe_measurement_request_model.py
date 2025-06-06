# external imports
from dataclasses import dataclass

# internal imports
from .base_definition_ripe_measurement_request_model import BaseDefinitionRIPEMeasurementRequestModel
from ..utilities.enums import DefinitionTypeRIPEMeasurementRequest


@dataclass(kw_only=True)
class PingDefinitionRIPEMeasurementRequestModel(BaseDefinitionRIPEMeasurementRequestModel):
    target: str
    type = DefinitionTypeRIPEMeasurementRequest.PING
