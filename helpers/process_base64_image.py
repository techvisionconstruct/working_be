import base64
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


def process_base64_image(base64_string: str) -> InMemoryUploadedFile:
    # Extract the base64 data if it includes the data URL prefix
    if "," in base64_string:
        base64_string = base64_string.split(",", 1)[1]

    # Decode and prepare the image data
    image_data = base64.b64decode(base64_string)
    image_io = io.BytesIO(image_data)
    image_io.seek(0)

    return InMemoryUploadedFile(
        file=image_io,
        field_name="image",
        name="image.png",
        content_type="image/png",  # Assuming PNG format
        size=len(image_data),
        charset=None,
    )
