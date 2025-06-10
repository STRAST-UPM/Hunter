# external imports
from pydantic import BaseModel

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
    # TODO change to polygon type
    intersection_area_polygon: str
    airports_in_intersection: list[AirportModel]
