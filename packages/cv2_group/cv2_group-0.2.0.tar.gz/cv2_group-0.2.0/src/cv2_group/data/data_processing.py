import logging
from typing import Tuple

import numpy as np
from patchify import patchify, unpatchify

import cv2

# Configure logging
logger = logging.getLogger(__name__)


def crop_image(image: np.ndarray) -> np.ndarray:
    """
    Crops the largest connected component from the image and centers it
    in a white square of size equal to the largest dimension.

    Parameters
    ----------
    image : np.ndarray
        Grayscale image as a 2D NumPy array.

    Returns
    -------
    np.ndarray
        Cropped and centered square image containing the largest component.
    """
    logger.info("Starting image cropping process.")

    # Apply median blur to reduce noise
    blurred_image = cv2.medianBlur(image, 5)

    # Apply thresholding to obtain binary image
    _, binary_image = cv2.threshold(blurred_image, 70, 200, cv2.THRESH_BINARY)

    # Identify connected components and their stats
    _, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image)

    # Find the largest non-background component
    max_area = 0
    max_index = -1
    for i in range(1, stats.shape[0]):
        area = stats[i, 4]
        if area > max_area:
            max_area = area
            max_index = i

    if max_index == -1:
        logger.error("No valid components found in the image.")
        raise ValueError("Could not find any non-background components.")

    x, y, width, height, _ = stats[max_index]
    size = max(width, height)

    # Create a square canvas and place the component in the center
    square_image = np.ones((size, size), dtype=np.uint8) * 255
    x_offset = (size - width) // 2
    y_offset = (size - height) // 2
    square_image[
        y_offset : y_offset + height, x_offset : x_offset + width
    ] = blurred_image[y : y + height, x : x + width]

    logger.info(f"Cropped and centered image to {size}x{size} square.")
    return square_image


def pad_image(
    image: np.ndarray, patch_size: int
) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    """
    Pads the image so its dimensions are divisible by patch_size by adding
    borders symmetrically.

    Parameters
    ----------
    image : np.ndarray
        Grayscale image as a 2D NumPy array.
    patch_size : int
        Size of the patches the image will be divided into.

    Returns
    -------
    Tuple[np.ndarray, Tuple[int, int, int, int]]
        Zero-padded image with height and width divisible by patch_size.
        A tuple containing padding sizes (top, bottom, left, right).
    """
    logger.info("Padding image to make its dimensions divisible by patch size.")

    # Get original image dimensions
    h, w = image.shape

    # Calculate the padding needed for each dimension
    height_padding = ((h // patch_size) + 1) * patch_size - h
    width_padding = ((w // patch_size) + 1) * patch_size - w

    # Split padding evenly between top/bottom and left/right
    top_padding = height_padding // 2
    bottom_padding = height_padding - top_padding
    left_padding = width_padding // 2
    right_padding = width_padding - left_padding

    # Apply zero padding to the image using OpenCV
    padded_image = cv2.copyMakeBorder(
        image,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_CONSTANT,
        value=0,
    )

    # Log the padding information
    logger.info(
        f"Padded image from ({h}, {w}) to {padded_image.shape} with "
        f"top={top_padding}, bottom={bottom_padding}, left={left_padding}, "
        f"right={right_padding}."
    )

    # Return padded image and the padding sizes
    return padded_image, (top_padding, bottom_padding, left_padding, right_padding)


def create_patches(
    image: np.ndarray, patch_size: int
) -> Tuple[np.ndarray, int, int, np.ndarray]:
    """
    Splits a grayscale image into non-overlapping square RGB patches of the
    given size.

    Parameters
    ----------
    image : np.ndarray
        Grayscale image as a 2D NumPy array.
    patch_size : int
        The height and width of each square patch.

    Returns
    -------
    np.ndarray
        4D array of shape (num_patches, patch_size, patch_size, 3), containing
        RGB patches.
    int
        Number of patch rows (i).
    int
        Number of patch columns (j).
    np.ndarray
        RGB version of the padded input image.
    """
    logger.info("Starting patch creation from grayscale image.")

    # Convert the grayscale image to a 3-channel RGB image by stacking
    petri_dish_padded_rgb = np.stack((image.squeeze(),) * 3, axis=-1)

    # Create non-overlapping patches using patchify
    patches = patchify(
        petri_dish_padded_rgb, (patch_size, patch_size, 3), step=patch_size
    )

    # Extract the number of patches in vertical (i) and horizontal (j) direction
    i = patches.shape[0]
    j = patches.shape[1]

    # Reshape the patches to a 4D array (num_patches, patch_size, patch_size, 3)
    patches = patches.reshape(-1, patch_size, patch_size, 3)

    logger.info(
        f"Created {len(patches)} patches of size {patch_size}x{patch_size}. "
        f"Grid: {i} rows x {j} cols."
    )

    return patches, i, j, petri_dish_padded_rgb


def unpatch_image(
    preds: np.ndarray, i: int, j: int, rgb_image: np.ndarray, patch_size: int
) -> np.ndarray:
    """
    Reconstructs the original grayscale prediction image from patches.

    Parameters
    ----------
    preds : np.ndarray
        3D array of shape (num_patches, patch_size, patch_size), containing
        grayscale predictions.
    i, j : int
        Patch grid dimensions, representing the number of patches along the
        height and width.
    rgb_image : np.ndarray
        The original RGB image used to determine the full output shape.
    patch_size : int
        The size of each square patch.

    Returns
    -------
    np.ndarray
        The reconstructed 2D grayscale prediction image.
    """
    logger.info("Reconstructing image from patches.")

    # Reshape the flat predictions array into the patch grid
    preds = preds.reshape(i, j, patch_size, patch_size)

    # Reconstruct the image using the unpatchify function
    predicted_mask = unpatchify(preds, (rgb_image.shape[0], rgb_image.shape[1]))

    # Log the shape of the reconstructed mask
    logger.info(f"Predicted mask shape: {predicted_mask.shape}")

    return predicted_mask


def remove_padding(
    image: np.ndarray, top: int, bottom: int, left: int, right: int
) -> np.ndarray:
    """
    Removes padding from an image based on the given top, bottom, left, and
    right values.

    Parameters
    ----------
    image : np.ndarray
        The padded image.
    top : int
        Number of pixels to remove from the top.
    bottom : int
        Number of pixels to remove from the bottom.
    left : int
        Number of pixels to remove from the left.
    right : int
        Number of pixels to remove from the right.

    Returns
    -------
    np.ndarray
        The cropped image without padding.
    """
    return image[top : image.shape[0] - bottom, left : image.shape[1] - right]
