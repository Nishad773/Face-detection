from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import StreamSession
from app.db.repositories.stream_session_repository import StreamSessionRepository


class StreamSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = StreamSessionRepository(session)

    async def get_or_create(self, source_id: str) -> StreamSession:
        stream_session = await self.repository.get_by_source_id(source_id)
        if stream_session is not None:
            return stream_session
        return await self.repository.create(source_id=source_id)

