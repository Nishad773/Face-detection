from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from app.schemas.roi import BoundingBox
from app.utils.image import load_rgb_image, save_jpeg_bytes


@dataclass(slots=True)
class FaceProcessingResult:
    bbox: BoundingBox | None
    image_bytes: bytes


class FaceDetectionService:
    def __init__(self, min_detection_confidence: float = 0.5) -> None:
        import mediapipe as mp

        self._detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=min_detection_confidence,
        )

    def detect_single_face(self, image_bytes: bytes) -> BoundingBox | None:
        image = load_rgb_image(image_bytes)
        image_array = np.asarray(image)
        result = self._detector.process(image_array)
        if not result.detections:
            return None

        detection = max(
            result.detections,
            key=lambda item: item.location_data.relative_bounding_box.width
            * item.location_data.relative_bounding_box.height,
        )
        return self._to_bbox(detection, image.width, image.height)

    def process_image(self, image_bytes: bytes) -> FaceProcessingResult:
        image = load_rgb_image(image_bytes)
        image_array = np.asarray(image)
        result = self._detector.process(image_array)
        if not result.detections:
            return FaceProcessingResult(bbox=None, image_bytes=save_jpeg_bytes(image))

        detection = max(
            result.detections,
            key=lambda item: item.location_data.relative_bounding_box.width
            * item.location_data.relative_bounding_box.height,
        )
        bbox = self._to_bbox(detection, image.width, image.height)
        processed = self._draw_bbox(image, bbox)
        return FaceProcessingResult(bbox=bbox, image_bytes=save_jpeg_bytes(processed))

    @staticmethod
    def _to_bbox(detection, image_width: int, image_height: int) -> BoundingBox:
        relative = detection.location_data.relative_bounding_box
        x = max(0, int(relative.xmin * image_width))
        y = max(0, int(relative.ymin * image_height))
        right = min(image_width, int((relative.xmin + relative.width) * image_width))
        bottom = min(image_height, int((relative.ymin + relative.height) * image_height))
        return BoundingBox(
            x=x,
            y=y,
            width=max(0, right - x),
            height=max(0, bottom - y),
        )

    @staticmethod
    def _draw_bbox(image: Image.Image, bbox: BoundingBox) -> Image.Image:
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle(
            [bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height],
            outline=(0, 255, 0),
            width=3,
        )
        return annotated
