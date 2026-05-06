# Real-Time Face Streaming System

Minimal full-stack app for real-time webcam frame streaming, server-side face detection without OpenCV, ROI persistence, and live processed-frame display.

## Stack

- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL
- Streaming: WebSockets
- Detection: MediaPipe + Pillow + NumPy
- Infra: Docker Compose

## Setup

1. Ensure Docker Desktop is running.
2. Create a local `.env` from `.env.example`.
3. From the project root, start the stack:

```bash
docker compose up --build
```

4. Open the app:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend health: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

5. Allow webcam access in the browser.

Use `.env.example` as the reference for local configuration.

## Architecture Summary

The browser captures webcam frames and sends them as base64 JPEG images to the backend over WebSocket. FastAPI decodes each frame, runs face detection with MediaPipe, draws a bounding box with Pillow, stores ROI metadata in PostgreSQL through SQLAlchemy, and returns the processed frame to the same socket client. The frontend renders the processed image and the latest ROI metadata.

Main backend layers:

- API layer: REST routes and WebSocket endpoint
- Services: stream orchestration, face detection, ROI persistence
- DB layer: SQLAlchemy models, repositories, Alembic migration
- Frontend: webcam capture, socket client, processed-frame view, ROI panel

## Endpoints

### REST

- `GET /api/v1/health`
  Returns app and database health.

- `GET /api/v1/roi/latest?session_id=<id>`
  Returns the latest ROI record for a stream session.

Example ROI response:

```json
{
  "id": 12,
  "session_id": 3,
  "timestamp": "2026-05-06T10:15:30.000000Z",
  "x": 120,
  "y": 84,
  "width": 160,
  "height": 160
}
```

### WebSocket

- `WS /api/v1/ws/ingest`
  Receives frames and replies with processed frames.

- `WS /api/v1/ws/stream`
  Present in the backend scaffold, but the current frontend flow uses `ws/ingest` directly for request/response streaming.

## WebSocket Flow

Client sends:

```json
{
  "frame_id": "frame-001",
  "source_id": "default",
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSk..."
}
```

Server replies:

```json
{
  "type": "processed_frame",
  "payload": {
    "frame_id": "frame-001",
    "source_id": "default",
    "session_id": 3,
    "image_base64": "/9j/4AAQSk...",
    "roi": {
      "x": 120,
      "y": 84,
      "width": 160,
      "height": 160
    },
    "detected_at": "2026-05-06T10:15:30.000000+00:00"
  }
}
```

If no face is detected, `roi` is `null` and the processed image is still returned.

## Docker Usage

Start everything:

```bash
docker compose up --build
```

Stop everything:

```bash
docker compose down
```

Stop and remove the database volume:

```bash
docker compose down -v
```

Services included in [docker-compose.yml](D:/Main-Project/docker-compose.yml):

- `postgres`
- `backend`
- `frontend`

The setup includes:

- named Postgres volume
- backend migration on startup with Alembic
- health checks for all three services
- env-driven config

## Tradeoffs

- Frames are sent as base64 JSON over WebSocket, which is simple but less efficient than binary frames.
- Face detection runs in-process in the backend, which keeps the design compact but limits horizontal scalability.
- The current flow returns processed frames on the ingest socket instead of using a separate dedicated output stream.
- PostgreSQL stores ROI metadata only, not full video frames, which keeps storage simpler and cheaper.
