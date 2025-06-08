# external imports

# internal imports
from .base_definition_ripe_measurement_request_model import BaseDefinitionRIPEMeasurementRequestModel
from ..utilities.enums import DefinitionTypeRIPEMeasurementRequest


class PingDefinitionRIPEMeasurementRequestModel(BaseDefinitionRIPEMeasurementRequestModel):
    target: str
    type = DefinitionTypeRIPEMeasurementRequest.PING
