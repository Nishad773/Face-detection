# Architecture Notes

## Runtime flow

1. Browser captures camera frames on a timer.
2. Browser compresses each frame as JPEG and sends it to the ingest WebSocket.
3. Backend decodes the frame to `Pillow.Image`.
4. Backend converts the image to `numpy.ndarray`.
5. Face detector returns one normalized bounding box.
6. Annotation service draws a rectangle on the frame.
7. ROI service stores bounding box coordinates and timestamps in PostgreSQL.
8. Stream service broadcasts:
   - processed frame payload
   - ROI metadata payload
9. Frontend renders the processed frame and latest ROI metadata.

## Detector choice

The initial implementation uses `face_recognition` because it is robust, well known, and avoids OpenCV. The detector is abstracted so `mediapipe`, `mtcnn`, or another implementation can be swapped later with minimal API-layer changes.

## Data model

`roi_records`

- `id`
- `frame_id`
- `source_id`
- `x`
- `y`
- `width`
- `height`
- `confidence`
- `detected_at`
- `created_at`

## Error handling strategy

- Validation failures return structured `4xx` responses for REST routes.
- Invalid WebSocket messages return error events instead of crashing the stream loop.
- Detector failures are logged with frame identifiers.
- DB write failures are isolated and reported while keeping stream connections alive when possible.

## Scalability path

- Replace in-process processing with a worker queue
- Add Redis pub/sub for fan-out
- Shard ingest by stream key
- Persist optional frame snapshots to object storage instead of PostgreSQL
