from keras import backend as K


def recall(y_true, y_pred):
    """
    Compute the recall score for binary classification.

    Recall is the ratio of true positives to the total number of actual positives:
    Recall = TP / (TP + FN)

    Parameters
    ----------
    y_true : tensor
        Ground truth binary labels (0 or 1).
    y_pred : tensor
        Predicted binary labels (0 or 1).

    Returns
    -------
    tensor
        Recall score as a scalar tensor.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())


def precision(y_true, y_pred):
    """
    Compute the precision score for binary classification.

    Precision is the ratio of true positives to the total number of predicted positives:
    Precision = TP / (TP + FP)

    Parameters
    ----------
    y_true : tensor
        Ground truth binary labels (0 or 1).
    y_pred : tensor
        Predicted binary labels (0 or 1).

    Returns
    -------
    tensor
        Precision score as a scalar tensor.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    return true_positives / (predicted_positives + K.epsilon())


def f1(y_true, y_pred):
    """
    Compute the F1 score for binary classification.

    The F1 score is the harmonic mean of precision and recall:
    F1 = 2 * (precision * recall) / (precision + recall)

    Parameters
    ----------
    y_true : tensor
        Ground truth binary labels (0 or 1).
    y_pred : tensor
        Predicted binary labels (0 or 1).

    Returns
    -------
    tensor
        F1 score as a scalar tensor.
    """
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    return 2 * ((prec * rec) / (prec + rec + K.epsilon()))
