# external imports
from pydantic import BaseModel, Field
from typing import Optional

# internal imports

class RipeMeasurementResponseModel(BaseModel):
    measurement: Optional[list[int]] = Field(alias="measurements", default=None)
    error: bool = False
