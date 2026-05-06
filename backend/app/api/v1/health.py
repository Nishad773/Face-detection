from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    database_status = "ok"
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "degraded"
    return HealthResponse(status="ok", database=database_status)
