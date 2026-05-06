import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.services.stream_service import StreamService
from app.streaming.connection_manager import stream_connection_manager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/ingest")
async def ingest_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    service = StreamService()
    try:
        while True:
            payload = await websocket.receive_json()
            response = await service.handle_ingest_payload(payload)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        logger.info("Ingest client disconnected.")
    except ValueError:
        logger.exception("Invalid image payload received.")
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({"type": "error", "payload": {"message": "Invalid frame payload."}})
    except Exception:
        logger.exception("Unhandled error in ingest socket.")
        try:
            await websocket.send_json({"type": "error", "payload": {"message": "Frame processing failed."}})
        finally:
            await websocket.close(code=1011)


@router.websocket("/ws/stream")
async def processed_stream(websocket: WebSocket) -> None:
    await stream_connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        stream_connection_manager.disconnect(websocket)
        logger.info("Processed stream client disconnected.")
