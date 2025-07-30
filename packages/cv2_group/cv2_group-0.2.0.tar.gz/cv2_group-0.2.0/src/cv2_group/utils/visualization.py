import matplotlib.pyplot as plt
import numpy as np

import cv2


def display_predicted_mask(pred_mask: np.ndarray) -> None:
    """
    Displays the predicted binary root mask.

    Parameters
    ----------
    pred_mask : np.ndarray
        Predicted mask (2D array or 3D with single channel).
    """
    if pred_mask.ndim == 3 and pred_mask.shape[-1] == 1:
        pred_mask = pred_mask[..., 0]
    elif pred_mask.ndim == 3 and pred_mask.shape[0] == 1:
        pred_mask = pred_mask[0]

    plt.figure(figsize=(8, 8))
    plt.title("Predicted Mask")
    plt.imshow(pred_mask, cmap="gray")
    plt.axis("off")
    plt.show()


def display_overlay(
    cropped_image: np.ndarray,
    predicted_mask: np.ndarray,
    alpha: float = 0.5,
    show: bool = True,
    return_png_bytes: bool = False,
) -> bytes | None:
    """
    Displays and optionally returns an overlay of the predicted root mask.

    Parameters
    ----------
    cropped_image : np.ndarray
        Original grayscale image (2D or 3D).
    predicted_mask : np.ndarray
        Binary predicted root mask (2D, values 0 or 255, dtype uint8).
    alpha : float
        Transparency factor for the overlay.
    show : bool
        Whether to show the image using matplotlib.
    return_png_bytes : bool
        If True, return the overlay image as PNG bytes (for FastAPI use).

    Returns
    -------
    bytes or None
        PNG image bytes if return_png_bytes is True, else None.
    """

    if len(cropped_image.shape) == 2:
        original_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2BGR)
    else:
        original_rgb = cropped_image.copy()

    # Create red overlay mask
    red_mask = np.zeros_like(original_rgb)
    red_mask[..., 2] = predicted_mask  # Apply binary mask to red channel

    # Blend the images
    overlay = cv2.addWeighted(original_rgb, 1 - alpha, red_mask, alpha, 0)

    # Display
    plt.figure(figsize=(8, 8))
    plt.title("Overlay: Predicted Roots on Original Image")
    plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

    # Create red mask and blend
    red_mask = np.zeros_like(original_rgb)
    red_mask[..., 2] = predicted_mask
    overlay = cv2.addWeighted(original_rgb, 1 - alpha, red_mask, alpha, 0)

    if show:
        plt.figure(figsize=(8, 8))
        plt.title("Overlay: Predicted Roots on Original Image")
        plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()

    if return_png_bytes:
        success, encoded_img = cv2.imencode(".png", overlay)
        if not success:
            raise ValueError("Failed to encode overlay image")
        return encoded_img.tobytes()

    return None
