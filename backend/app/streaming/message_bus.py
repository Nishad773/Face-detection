from app.streaming.connection_manager import stream_connection_manager


class MessageBus:
    async def publish(self, payload: dict) -> None:
        await stream_connection_manager.broadcast_json(payload)


message_bus = MessageBus()

