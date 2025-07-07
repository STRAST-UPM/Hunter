# external imports
from pydantic import BaseModel
from typing import Optional

# internal imports
from .hop_response_model import HopResponseModel

class TracerouteHopModel(BaseModel):
    id: int
    hop_position: int

    hop_responses: Optional[list[HopResponseModel]] = None