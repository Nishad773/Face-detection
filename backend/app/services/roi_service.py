from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ROIRecord
from app.db.repositories.roi_repository import ROIRepository
from app.schemas.roi import BoundingBox, ROIResponse


class ROIService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ROIRepository(session)

    async def create(self, session_id: int, bbox: BoundingBox) -> ROIResponse:
        record = ROIRecord(
            session_id=session_id,
            timestamp=datetime.now(timezone.utc),
            x=bbox.x,
            y=bbox.y,
            width=bbox.width,
            height=bbox.height,
        )
        created = await self.repository.create(record)
        return ROIResponse.model_validate(created)

    async def get_latest(self, session_id: int) -> ROIResponse | None:
        record = await self.repository.get_latest(session_id)
        if record is None:
            return None
        return ROIResponse.model_validate(record)
