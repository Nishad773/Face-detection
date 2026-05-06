from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import StreamSession


class StreamSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_source_id(self, source_id: str) -> StreamSession | None:
        statement = select(StreamSession).where(StreamSession.source_id == source_id).limit(1)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, source_id: str) -> StreamSession:
        stream_session = StreamSession(source_id=source_id)
        self.session.add(stream_session)
        await self.session.commit()
        await self.session.refresh(stream_session)
        return stream_session

