import base64
import io
import logging

import PIL.Image

logger = logging.getLogger(__name__)

def validate_base64_image(base64_string: str) -> bool:
    """Validate if a string is a valid base64-encoded image.

    Args:
        base64_string: The base64 string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        # Try to decode base64
        image_data = base64.b64decode(base64_string)

        # Try to open as image
        with PIL.Image.open(io.BytesIO(image_data)) as img:
            logger.debug(
                f"Validated base64 image, format: {img.format}, size: {img.size}"
            )
            return True

    except Exception as e:
        logger.warning(f"Invalid base64 image: {str(e)}")
        return False
