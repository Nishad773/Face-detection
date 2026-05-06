from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.roi import BoundingBox


class FrameIngestMessage(BaseModel):
    frame_id: str
    source_id: str = "default"
    image_base64: str
    sent_at: datetime | None = None


class ProcessedFrameMessage(BaseModel):
    type: str = Field(default="processed_frame")
    frame_id: str
    source_id: str
    session_id: int
    image_base64: str
    roi: BoundingBox | None = None
    detected_at: datetime | None = None


class StreamEvent(BaseModel):
    type: str
    payload: dict
