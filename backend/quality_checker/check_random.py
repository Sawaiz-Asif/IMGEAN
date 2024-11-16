import random

def check_random(img, *args) -> bool:
    """
    Returns True or False randomly based on a percentage.
    Args:
        img: The input image as a NumPy array.
        *args: Optional percentage (0 to 100). Default is 50.
    Returns:
        bool: True or False based on the random percentage.
    """
    percentage = args[0] if args else 50
    return random.uniform(0, 100) < percentage
