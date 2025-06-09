# external imports
import json
from pydantic import BaseModel

# internal imports
from src.utilities.enums import AddressFamilyRIPEMeasurementRequest
from src.utilities.enums import DefinitionTypeRIPEMeasurementRequest


class BaseTestModel(BaseModel):
    # mandatory ones
    target: str
    description: str
    af: AddressFamilyRIPEMeasurementRequest = AddressFamilyRIPEMeasurementRequest.IPV4
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


class TestModel(BaseTestModel):
    type: DefinitionTypeRIPEMeasurementRequest = DefinitionTypeRIPEMeasurementRequest.TRACEROUTE


test1 = BaseTestModel(
    target="hola",
    description="hola",
    type=DefinitionTypeRIPEMeasurementRequest.TRACEROUTE,
)

test2 = TestModel(
    target="hola",
    description="hola",
)

print(
    json.dumps(test1.model_dump(), indent=4)
)
