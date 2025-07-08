# external imports
from pydantic import BaseModel
from shapely import Polygon, wkt

# internal imports
from .airport_model import AirportModel


class TrackResultModel(BaseModel):
    origin_country: str
    origin_latitude: float
    origin_longitude: float
    destination_country: str
    destination_city: str
    destination_latitude: float
    destination_longitude: float
    intersection_area_polygon: str

    airports_in_intersection: list[AirportModel]

    def get_intersection_area_polygon(self) -> Polygon:
        return Polygon(wkt.loads(self.intersection_area_polygon))

    def set_intersection_area_polygon(self, area: Polygon):
        self.intersection_area_polygon = area.wkt
