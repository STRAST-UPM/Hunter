# external imports
from pydantic import BaseModel
# from datetime import datetime

# internal imports
from ..utilities.enums import AddressFamilyRIPEMeasurementRequest
from ..utilities.enums import DefinitionTypeRIPEMeasurementRequest


class BaseDefinitionRIPEMeasurementRequestModel(BaseModel):
    # mandatory ones
    description: str
    af: AddressFamilyRIPEMeasurementRequest
    type: DefinitionTypeRIPEMeasurementRequest
    # optional, default values
    resolve_on_probe: bool = False
    skip_dns_check: bool = False
    is_oneoff: bool = True

    # TODO check if necessary to have for oneoff measurements
    # start_time: datetime = None

    # not relevant for the moment
    # stop_time: datetime = None

    # not relevant in oneoff measurements
    # interval

    # not used, related to interval
    # spread

    is_public: bool = True
