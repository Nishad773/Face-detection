import asyncio
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class StreamConnectionManager:
    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def startup(self) -> None:
        logger.info("Stream connection manager started.")

    async def shutdown(self) -> None:
        async with self._lock:
            connections = list(self.active_connections)
            self.active_connections.clear()
        for connection in connections:
            await connection.close()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)

    async def broadcast_json(self, payload: dict) -> None:
        stale_connections: list[WebSocket] = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(payload)
            except Exception:
                logger.exception("Broadcast failed for a websocket connection.")
                stale_connections.append(connection)

        for connection in stale_connections:
            self.disconnect(connection)


stream_connection_manager = StreamConnectionManager()

