# external imports

# internal imports
from .traceroute_hop_model import TracerouteHopModel
from .base_measurement_result_model import BaseMeasurementResultModel


class TracerouteModel(BaseMeasurementResultModel):
    destination_ip: str
    destination_name: str

    hops: list[TracerouteHopModel]
