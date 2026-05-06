from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.roi import router as roi_router
from app.api.v1.streams import router as streams_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(roi_router, prefix="/roi", tags=["roi"])
api_router.include_router(streams_router, tags=["streams"])

