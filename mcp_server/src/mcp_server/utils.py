import base64
import io
import numpy as np
from PIL import Image
from io import BytesIO

def ndarray_to_base64(image_data: np.ndarray) -> str:
    """Convierte los datos de la imagen (matriz de píxeles) a base64."""
    # Convertir la matriz numpy (image_data) a una imagen
    image = Image.fromarray(image_data.astype(np.uint8))
    
    # Crear un buffer en memoria para guardar la imagen
    buffered = BytesIO()
    # Guardar la imagen en el buffer como JPEG
    image.save(buffered, format="JPEG")
    
    # Convertir el buffer en base64
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


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

def base64_to_ndarray(b64: str) -> np.ndarray:
    """
    Decode a base64-encoded string to a NumPy array.

    Args:
        b64 (str): The base64-encoded string.

    Returns:
        np.ndarray: The decoded NumPy array.
    """
    img_bytes = base64.b64decode(b64)

    # Open image with Pillow
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")  # ensure 3 channels

    # Convert to NumPy array
    img_array = np.array(img)

    return img_array
