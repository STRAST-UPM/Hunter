# external imports
from pydantic import BaseModel

# internal imports


class TrackStartResponseModel(BaseModel):
    track_id: int
