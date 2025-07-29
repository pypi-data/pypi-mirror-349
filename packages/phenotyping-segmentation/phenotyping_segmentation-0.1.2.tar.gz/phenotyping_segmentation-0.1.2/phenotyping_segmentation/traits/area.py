import numpy as np


def get_area_pixel(img):
    """Get area or total number of pixels.

    Args:
        img: root segmentation image as array.

    Returns:
        number of root pixels.
    """
    return np.count_nonzero(img)
