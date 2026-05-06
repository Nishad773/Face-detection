from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schemas.roi import ROIResponse
from app.services.roi_service import ROIService

router = APIRouter()


@router.get("/latest", response_model=ROIResponse)
async def get_latest_roi(
    session_id: int = Query(..., gt=0),
    session: AsyncSession = Depends(get_db_session),
) -> ROIResponse:
    service = ROIService(session)
    roi = await service.get_latest(session_id=session_id)
    if roi is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ROI found for session.")
    return roi
