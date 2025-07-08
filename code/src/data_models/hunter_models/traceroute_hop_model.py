# external imports
from pydantic import BaseModel, Field
from typing import Optional

# internal imports
from .hop_response_model import HopResponseModel

class TracerouteHopModel(BaseModel):
    hop_position: int

    hop_responses: list[HopResponseModel]
