import numpy as np


def check_missing(prediction_res_arr, epsilon):
    """
    Since Unet uses pixel segmentation, we can check if all classes of heart is available or not.
    Shape of prediction_arr: (x, y, z)
    """
    contain = set()
    for value, count in np.unique(prediction_res_arr, retrun_counts=True):
        pass
