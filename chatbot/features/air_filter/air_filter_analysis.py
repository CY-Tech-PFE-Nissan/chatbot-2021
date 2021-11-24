import math
import io
from pathlib import Path
import cv2
from PIL import Image
import numpy as np
from scipy.stats import wasserstein_distance

ctrl_img_path = Path(__file__).resolve().parent / "data" / "control_img.JPG"


def transform_images(img_bytes):
    """Transforms images from bytes to np.ndarray

    Parameter
    ---------
    img_bytes: bytes

    Returns
    -------
    np.ndarray
        Preprocessed grayscaled image (value between 0 and 1).
    """
    image = Image.open(io.BytesIO(img_bytes)).convert("L")
    return np.array(image) / 255


def get_analysis(img_bytes):
    """Predicts wear percentage based on an image (as bytes)

    Parameter
    ---------
    img_bytes: bytes

    Returns
    -------
    float
        predicted wear percentage
    """
    # All these data are provided by Nissan's lab
    wear_pct = {
        10: 4.1,
        20: 8.3,
        30: 16.5,
        40: 25,
        50: 33,
        60: 45,
        70: 50,
        80: 66,
        90: 87,
        100: 100,
    }

    coef_ = 0.00133038
    intercept_ = 0.05712002

    # Loading control image
    ctrl_img = cv2.imread(str(ctrl_img_path), cv2.IMREAD_GRAYSCALE) / 255
    ctrl_img = ctrl_img.flatten()
    # Preprocessing image
    img = transform_images(img_bytes)
    img = img.flatten()

    # Computing dust_level based on distance and known coefficients
    distance = wasserstein_distance(ctrl_img, img)
    dust_level = (distance - intercept_) / coef_

    # To prevent bugs if the image is absolutely not an air filter image
    if dust_level >= 100:
        return str(100)

    # Computing new coefficients to get the wear percentage
    low = min(100, max(0, math.floor(dust_level / 10) * 10))
    high = min(100, max(0, math.ceil(dust_level / 10) * 10))

    coef_ = (wear_pct[low] - wear_pct[high]) / (low - high)
    intercept_ = wear_pct[low] - low * coef_

    pred_wear_pct = (dust_level * coef_) + intercept_

    return str(round(pred_wear_pct, 2))
