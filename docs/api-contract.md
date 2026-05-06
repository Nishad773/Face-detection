# API Contract

## REST endpoints

### `GET /api/v1/health`

Response:

```json
{
  "status": "ok"
}
```

### `GET /api/v1/roi/latest?source_id=default`

Success response:

```json
{
  "frame_id": "frame-001",
  "source_id": "default",
  "x": 120,
  "y": 84,
  "width": 160,
  "height": 160,
  "confidence": null,
  "detected_at": "2026-05-06T10:15:30.000000Z",
  "created_at": "2026-05-06T10:15:30.000000Z"
}
```

Not found response:

```json
{
  "detail": "No ROI found for source."
}
```

## WebSockets

### `WS /api/v1/ws/ingest`

Client sends:

```json
{
  "frame_id": "frame-001",
  "source_id": "default",
  "image_base64": "/9j/4AAQSkZJRgABAQ..."
}
```

### `WS /api/v1/ws/stream`

Server sends processed events:

```json
{
  "type": "processed_frame",
  "payload": {
    "frame_id": "frame-001",
    "source_id": "default",
    "image_base64": "/9j/4AAQSkZJRgABAQ...",
    "roi": {
      "x": 120,
      "y": 84,
      "width": 160,
      "height": 160,
      "confidence": null
    },
    "detected_at": "2026-05-06T10:15:30.000000Z"
  }
}
```

Error event shape:

```json
{
  "type": "error",
  "payload": {
    "message": "Invalid frame payload"
  }
}
```

