import logging

import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.graph import route_through_array
from skimage.morphology import skeletonize
from skimage.segmentation import watershed

import cv2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def separate_merged_roots(mask, expected_plants=5):
    """
    Separate merged root regions in a binary mask using the watershed algorithm.

    Parameters
    ----------
    mask : np.ndarray
        Binary mask where roots are marked as foreground (non-zero values).
    expected_plants : int
        Estimated number of individual root systems in the mask.

    Returns
    -------
    np.ndarray
        Labeled mask where each root instance is assigned a unique integer.
    """
    distance = ndi.distance_transform_edt(mask)
    min_distance = mask.shape[1] // (expected_plants * 2)
    top_portion = mask.shape[0] // 4
    distance_top = distance.copy()
    distance_top[top_portion:, :] = 0

    coords = peak_local_max(
        distance_top, min_distance=min_distance, num_peaks=expected_plants
    )

    markers = np.zeros_like(mask, dtype=int)
    for i, (x, y) in enumerate(coords, start=1):
        markers[x, y] = i

    labels = watershed(-distance, markers, mask=mask)
    return labels


def process_predicted_mask(predicted_mask, use_watershed=True, expected_plants=5):
    """
    Process a binary mask to generate labeled root instances.

    Parameters
    ----------
    predicted_mask : np.ndarray
        Binary mask predicted by the model.
    use_watershed : bool
        Whether to apply watershed-based separation of roots.
    expected_plants : int
        Number of root instances expected.

    Returns
    -------
    tuple
        A tuple of:
        - binary_mask (np.ndarray)
        - label_ids (np.ndarray)
        - totalLabels (int)
        - stats (np.ndarray)
        - centroids (np.ndarray)
    """
    binary_mask = np.array(predicted_mask, dtype=np.uint8)

    if use_watershed:
        label_ids = separate_merged_roots(binary_mask, expected_plants)
        totalLabels = label_ids.max() + 1
        retval, _, stats, centroids = cv2.connectedComponentsWithStats(
            np.uint8(label_ids > 0)
        )
    else:
        retval, label_ids, stats, centroids = cv2.connectedComponentsWithStats(
            binary_mask
        )
        totalLabels = retval

    return binary_mask, label_ids, totalLabels, stats, centroids


def find_labels_in_rois(label_ids, totalLabels, stats, centroids, rois):
    """
    Identify root labels within defined regions of interest (ROIs).

    Parameters
    ----------
    label_ids : np.ndarray
        Labeled image where each root has a unique label ID.
    totalLabels : int
        Total number of labels found.
    stats : np.ndarray
        Connected component statistics array.
    centroids : np.ndarray
        Coordinates of object centroids.
    rois : list of tuples
        List of ROIs defined as (x, y, width, height).

    Returns
    -------
    tuple
        Dictionary and list of max height label IDs in each ROI.
    """
    max_label_dict = {}
    max_label_list = []
    counter = 0

    for roi in rois:
        key = f"label_{counter}"
        counter += 1
        x, y, width, height = roi
        x_end, y_end = x + width, y + height

        indices_in_roi = []
        for i in range(1, totalLabels):
            label_x = stats[i, cv2.CC_STAT_LEFT]
            label_y = stats[i, cv2.CC_STAT_TOP]
            label_width = stats[i, cv2.CC_STAT_WIDTH]
            label_height = stats[i, cv2.CC_STAT_HEIGHT]
            label_x_end = label_x + label_width
            label_y_end = label_y + label_height

            if not (
                x_end < label_x or label_x_end < x or
                y_end < label_y or label_y_end < y
            ):
                indices_in_roi.append(i)

        if indices_in_roi:
            max_height_label = max(
                indices_in_roi, key=lambda idx: stats[idx, cv2.CC_STAT_HEIGHT]
            )
            max_label_list.append(max_height_label)
            max_label_dict[key] = max_height_label
            print(
                f"ROI {roi}: Label {max_height_label} has the highest height: "
                f"{stats[max_height_label, cv2.CC_STAT_HEIGHT]}"
            )
        else:
            max_label_dict[key] = None
            print(f"ROI {roi}: No labels found.")

    return max_label_dict, max_label_list


def extract_root_instances(label_ids, max_label_dict):
    """
    Extract binary masks for individual root instances from a labeled image.

    Parameters
    ----------
    label_ids : np.ndarray
        Labeled image where each label represents a root.
    max_label_dict : dict
        Dictionary of labels to extract, keyed by instance name.

    Returns
    -------
    list of np.ndarray
        List of binary masks, one for each root instance.
    """
    root_instances = []
    for label_name, label_id in max_label_dict.items():
        label_mask = np.where(label_ids == label_id, 1, 0)
        root_instances.append(label_mask)
    return root_instances


def analyze_primary_root(root_instances):
    """
    Analyze the primary root of each binary mask instance.

    Uses skeletonization and shortest-path tracing to extract geometric properties
    of each root such as length, base, tip, and traced path.

    Parameters
    ----------
    root_instances : list of np.ndarray
        Binary masks (1 = root, 0 = background) for each root instance.

    Returns
    -------
    list of dict
        One dictionary per root with:
        - 'length' (float): Euclidean path length in pixels.
        - 'tip_coords' (tuple): (row, col) of the root tip.
        - 'base_coords' (tuple): (row, col) of the root base.
        - 'primary_path' (np.ndarray): Array of (row, col) path coordinates.
    """
    results = []

    for idx, root in enumerate(root_instances):
        logger.info(f"Analyzing root instance {idx}.")
        skeleton = skeletonize(root)

        if np.any(skeleton):
            coords = np.where(skeleton > 0)
            if len(coords[0]) == 0:
                logger.error("Skeleton has no coordinates. Skipping this root.")
                results.append(
                    {
                        "length": 0,
                        "tip_coords": None,
                        "base_coords": None,
                        "primary_path": None,
                    }
                )
                continue

            highest_y = min(coords[0])
            lowest_y = max(coords[0])
            highest_x_candidates = coords[1][coords[0] == highest_y]
            lowest_x_candidates = coords[1][coords[0] == lowest_y]

            if highest_x_candidates.size == 0 or lowest_x_candidates.size == 0:
                logger.error("Unable to determine extremities.")
                results.append(
                    {
                        "length": 0,
                        "tip_coords": None,
                        "base_coords": None,
                        "primary_path": None,
                    }
                )
                continue

            highest_x = highest_x_candidates[0]
            lowest_x = lowest_x_candidates[0]
            base = (highest_y, highest_x)
            tip = (lowest_y, lowest_x)

            costs = np.where(skeleton, 1, 1000000)

            try:
                path_coords, path_cost = route_through_array(
                    costs, start=base, end=tip, fully_connected=True
                )
                path_coords = np.array(path_coords)

                length = np.sum(
                    np.sqrt(np.sum(np.diff(path_coords, axis=0) ** 2, axis=1))
                )

                results.append(
                    {
                        "length": length,
                        "tip_coords": tip,
                        "base_coords": base,
                        "primary_path": path_coords,
                    }
                )
            except Exception as e:
                logger.error(f"Pathfinding failed with error: {e}")
                results.append(
                    {
                        "length": 0,
                        "tip_coords": None,
                        "base_coords": None,
                        "primary_path": None,
                    }
                )
        else:
            logger.error("Skeleton contains no valid path.")
            results.append(
                {
                    "length": 0,
                    "tip_coords": None,
                    "base_coords": None,
                    "primary_path": None,
                }
            )

    logger.info("Finished analyzing all root instances.")
    return results

