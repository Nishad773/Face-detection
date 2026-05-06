from types import SimpleNamespace

from PIL import Image

from app.schemas.roi import BoundingBox
from app.services.face_detection_service import FaceDetectionService
from app.utils.image import save_jpeg_bytes


def test_drawn_image_bytes_are_returned() -> None:
    service = FaceDetectionService.__new__(FaceDetectionService)
    image = Image.new("RGB", (32, 32), "black")
    payload = save_jpeg_bytes(image)

    service._detector = SimpleNamespace(
        process=lambda _: SimpleNamespace(
            detections=[
                SimpleNamespace(
                    location_data=SimpleNamespace(
                        relative_bounding_box=SimpleNamespace(
                            xmin=0.25,
                            ymin=0.25,
                            width=0.5,
                            height=0.5,
                        )
                    )
                )
            ]
        )
    )

    result = service.process_image(payload)

    assert isinstance(result.bbox, BoundingBox)
    assert result.bbox.width > 0
    assert result.bbox.height > 0
    assert isinstance(result.image_bytes, bytes)
    assert len(result.image_bytes) > 0
