# external imports
from pydantic import BaseModel, Field
from typing import Optional

# internal imports

class RipeMeasurementResponseModel(BaseModel):
    measurement_list_id: list[int] = Field(alias="measurements")
    error_msg: Optional[str] = None
