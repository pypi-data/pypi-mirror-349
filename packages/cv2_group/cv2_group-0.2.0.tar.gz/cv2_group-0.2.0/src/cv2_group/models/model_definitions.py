# Imports
import logging

from tensorflow.keras.models import load_model

from cv2_group.utils.helpers import f1

# Configure logging
logger = logging.getLogger(__name__)


def load_trained_model(model_path):
    """
    Load a trained Keras model from the specified file path.

    Parameters
    ----------
    model_path : str
        The path to the saved Keras model file.

    Returns
    -------
    keras.models.Model
        The loaded Keras model.

    """
    logger.info("Loading trained model...")
    model = load_model(model_path, custom_objects={"f1": f1}, compile=False)
    logger.info("Model loaded successfully.")
    return model
