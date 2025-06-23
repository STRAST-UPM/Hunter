# external imports
from shapely import Polygon

# internal imports
from .base_measurement_result_model import BaseMeasurementResultModel

class PingModel(BaseMeasurementResultModel):
    destination_ip: str
    destination_name: str
    max_rtt_ms: float
    min_rtt_ms: float
    average_rtt_ms: float
    coverage_area_polygon: Polygon
