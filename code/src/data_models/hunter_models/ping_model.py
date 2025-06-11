# external imports
from pydantic import BaseModel
from datetime import datetime

# internal imports
from .base_measurement_result_model import BaseMeasurementResultModel

class PingModel(BaseMeasurementResultModel):
    destination_ip: str
    destination_name: str
    max_rtt_ms: float
    min_rtt_ms: float
    average_rtt_ms: float
    # TODO change to polygon type
    coverage_area_polygon: str
