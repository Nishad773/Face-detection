from __future__ import annotations

from io import BytesIO

from PIL import Image


def load_rgb_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_bytes))
    image.load()
    return image.convert("RGB")


def save_jpeg_bytes(image: Image.Image, quality: int = 85) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    return buffer.getvalue()

