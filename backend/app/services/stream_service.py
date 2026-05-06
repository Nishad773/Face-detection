import logging
from asyncio import to_thread
from base64 import b64decode, b64encode

from app.db.session import async_session_factory
from app.schemas.stream import FrameIngestMessage
from app.services.face_detection_service import FaceDetectionService
from app.services.roi_service import ROIService
from app.services.stream_session_service import StreamSessionService

logger = logging.getLogger(__name__)


class StreamService:
    def __init__(self) -> None:
        self.face_detection_service = FaceDetectionService()

    async def handle_ingest_payload(self, payload: dict) -> dict:
        message = FrameIngestMessage.model_validate(payload)
        image_bytes = self._decode_base64_image(message.image_base64)
        result = await to_thread(self.face_detection_service.process_image, image_bytes)

        async with async_session_factory() as db_session:
            stream_session = await StreamSessionService(db_session).get_or_create(message.source_id)
            detected_at = None
            roi_payload = None
            if result.bbox is not None:
                roi = await ROIService(db_session).create(session_id=stream_session.id, bbox=result.bbox)
                detected_at = roi.timestamp
                roi_payload = result.bbox.model_dump()

        response = {
            "type": "processed_frame",
            "payload": {
                "frame_id": message.frame_id,
                "source_id": message.source_id,
                "session_id": stream_session.id,
                "image_base64": b64encode(result.image_bytes).decode("utf-8"),
                "roi": roi_payload,
                "detected_at": detected_at.isoformat() if detected_at else None,
            },
        }
        logger.debug("Processed frame %s for source %s", message.frame_id, message.source_id)
        return response

    @staticmethod
    def _decode_base64_image(value: str) -> bytes:
        if "," in value:
            _, value = value.split(",", 1)
        return b64decode(value)
