from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class ROIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    timestamp: datetime
    x: int
    y: int
    width: int
    height: int
