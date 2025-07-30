import logging

logger = logging.getLogger(__name__)


def predict_root(patches, model):
    preds = model.predict(patches / 255)
    return preds
