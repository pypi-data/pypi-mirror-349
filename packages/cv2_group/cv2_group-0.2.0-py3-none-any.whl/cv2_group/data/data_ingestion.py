import logging

import numpy as np

import cv2

# Configure logging
logger = logging.getLogger(__name__)


def load_image(image_path: str) -> np.ndarray:
    """
    Loads an image from the given file path and converts it to grayscale.

    Parameters
    ----------
    image_path : str
        The path to the image file to be loaded.

    Returns
    -------
    np.ndarray
        The grayscale image as a 2D NumPy array.

    Raises
    ------
    FileNotFoundError
        If the image could not be loaded from the specified path.
    """
    logging.info(f"Attempting to load image from path: {image_path}")

    # Load the image in grayscale
    grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded correctly
    if grayscale_image is None:
        logging.error(f"Failed to load image from path: {image_path}")
        raise FileNotFoundError(f"Could not load the image at {image_path}")

    logging.info(f"Image successfully loaded from path: {image_path}")
    return grayscale_image
