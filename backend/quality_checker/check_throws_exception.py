def check_throws_exception(img, *args) -> bool:
    """
    Always throws an exception.
    Args:
        img: The input image as a NumPy array.
        *args: Unused.
    Throws:
        Exception
    """
    raise Exception("Something went wrong!")