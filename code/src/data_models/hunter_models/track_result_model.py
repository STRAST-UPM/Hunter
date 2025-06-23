# external imports
from pydantic import BaseModel
from shapely import Polygon

# internal imports
from .airport_model import AirportModel


class TrackResultModel(BaseModel):
    id: int
    origin_country: str
    origin_latitude: float
    origin_longitude: float
    destination_country: str
    destination_city: str
    destination_latitude: float
    destination_longitude: float
    intersection_area_polygon: Polygon

    airports_in_intersection: list[AirportModel]
