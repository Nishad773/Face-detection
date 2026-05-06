from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ROIRecord


class ROIRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, roi: ROIRecord) -> ROIRecord:
        self.session.add(roi)
        await self.session.commit()
        await self.session.refresh(roi)
        return roi

    async def get_latest(self, session_id: int) -> ROIRecord | None:
        statement = (
            select(ROIRecord)
            .where(ROIRecord.session_id == session_id)
            .order_by(ROIRecord.timestamp.desc())
            .limit(1)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
