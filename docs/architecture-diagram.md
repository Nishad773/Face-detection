# Architecture Diagram Plan

Generate a diagram showing:

1. React frontend
2. Ingest WebSocket from browser to FastAPI backend
3. Processed stream WebSocket from backend to browser
4. REST ROI endpoint from browser to backend
5. Face detection and annotation services inside backend
6. PostgreSQL connected to SQLAlchemy repository layer
7. Docker Compose wrapping frontend, backend, and database

Suggested diagram layout:

- Left: frontend browser client
- Center: FastAPI service with internal layers
- Right: PostgreSQL
- Bottom: Docker Compose orchestration boundary
