# external imports
from pydantic import BaseModel

# internal imports


class TrackStartReponseModel(BaseModel):
    track_id: int
