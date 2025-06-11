# external imports
from pydantic import BaseModel

# internal imports
from .hop_response_model import HopResponseModel

class TracerouteHopModel(BaseModel):
    id: int
    hop_position: int

    hop_responses: list[HopResponseModel]