# external imports
from pydantic import BaseModel
from typing import Optional

# internal imports


class AirportModel(BaseModel):
    iata_code: str
    size: Optional[str] = None
    name: str
    latitude: float
    longitude: float
    country_code: str
    city_name: str
