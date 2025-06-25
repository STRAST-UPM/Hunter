# external imports
from shapely import Polygon, wkt

# internal imports
from .base_measurement_result_model import BaseMeasurementResultModel

class PingModel(BaseMeasurementResultModel):
    destination_ip: str
    destination_name: str
    max_rtt_ms: float
    min_rtt_ms: float
    average_rtt_ms: float
    coverage_area_polygon: str

    def get_coverage_area_polygon(self) -> Polygon:
        return Polygon(wkt.loads(self.coverage_area_polygon))

    def set_coverage_area_polygon(self, area: Polygon):
        self.coverage_area_polygon = area.wkt
