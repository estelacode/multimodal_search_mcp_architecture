import base64
import io
from PIL import Image
def base64_to_pil_image(b64: str) -> Image.Image:
    
    """
    Decodes a base64-encoded string to a PIL Image object.

    Args:
        b64 (str): The base64-encoded string.

    Returns:
        Image.Image: The decoded PIL Image object.
    """
    img_bytes = base64.b64decode(b64)

    # Open image with Pillow
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")  # ensure 3 channels

    return img


def image_to_base64(image_path: str) -> str:
    """
    Convert an image at the given path to a base64-encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64-encoded image string.
    """
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
    return base64_image
