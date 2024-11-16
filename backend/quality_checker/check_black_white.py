import numpy as np

def check_black_white(img, *args) -> bool:
    """
    Checks if the image is black and white.
    Args:
        img: The input image as a NumPy array.
        *args: Optional threshold percentage (0 to 100). Default is 0.
    Returns:
        bool: True if the image is black and white within the threshold, False otherwise.
    """
    threshold = args[0] if args else 0
    grayscale = np.allclose(img, img.mean(axis=-1, keepdims=True), atol=threshold / 100)
    return grayscale