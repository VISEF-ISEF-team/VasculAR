import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from glob import glob
from tqdm import tqdm
from tensorflow.keras.utils import CustomObjectScope
from sklearn.metrics import f1_score, jaccard_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import nibabel as nib
import os
import re

smooth = 1e-15


def dice_coef(y_true, y_pred):
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)


def dice_coef_numpy(y_true, y_pred):
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()
    intersection = np.sum(y_true * y_pred)
    dice = (2 * intersection + smooth) / (np.sum(y_true) + np.sum(y_pred))
    return dice


def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)


def dice_score(y_true, y_pred, class_id):
    """
    Arrays are already flatten 
    """

    if class_id in np.unique(y_true):
        y_true = np.array(np.where(y_true == class_id, 1, 0), dtype=np.float32)
        y_pred = np.array(np.where(y_pred == class_id, 1, 0), dtype=np.float32)
    else:
        y_true = np.array(np.where(y_true == class_id, 0, 1), dtype=np.float32)
        y_pred = np.array(np.where(y_pred == class_id, 0, 1), dtype=np.float32)

    intersection = tf.reduce_sum(y_true * y_pred)

    denominator = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth
    return (2. * intersection + smooth) / denominator


def dice_score_per_class(y_true, y_pred, num_classes):
    dice_scores = []
    for class_id in range(num_classes):
        dice = dice_score(y_true, y_pred, class_id).numpy()
        dice_scores.append(dice)
    return dice_scores


def convert_multiclass_to_binary_mask(a: np.array):
    uniques = sorted(np.unique(a))

    for num in uniques:
        if num == 0:
            continue
        elif num == 1:
            continue
        elif num > 1:
            a[a == num] = 1


def extract_label_number(path):
    # Extract the label number from the file name using regular expression
    match = re.search(r'ct_\d+_label_(\d+)\.nii', path)
    if match:
        return int(match.group(1))
    else:
        return -1  # Return -1 if no label number is found


def save_whole_mask(mask_path: str):
    separate_mask_path = sorted(
        glob(os.path.join(mask_path, "output", "*.nii")), key=extract_label_number)

    """Get labels from .nii files"""
    label_1 = np.uint(nib.load(separate_mask_path[1]).get_fdata())
    label_2 = np.uint(nib.load(separate_mask_path[2]).get_fdata())
    label_3 = np.uint(nib.load(separate_mask_path[3]).get_fdata())
    label_4 = np.uint(nib.load(separate_mask_path[4]).get_fdata())
    label_5 = np.uint(nib.load(separate_mask_path[5]).get_fdata())
    label_6 = np.uint(nib.load(separate_mask_path[6]).get_fdata())
    label_7 = np.uint(nib.load(separate_mask_path[7]).get_fdata())
    label_8 = np.uint(nib.load(separate_mask_path[8]).get_fdata())
    label_9 = np.uint(nib.load(separate_mask_path[9]).get_fdata())
    label_10 = np.uint(nib.load(separate_mask_path[10]).get_fdata())
    label_11 = np.uint(nib.load(separate_mask_path[11]).get_fdata())

    label_0 = np.ones((600, 600, 512))

    """Convert to binary (0, 1)"""
    convert_multiclass_to_binary_mask(label_1)
    convert_multiclass_to_binary_mask(label_2)
    convert_multiclass_to_binary_mask(label_3)
    convert_multiclass_to_binary_mask(label_4)
    convert_multiclass_to_binary_mask(label_5)
    convert_multiclass_to_binary_mask(label_6)
    convert_multiclass_to_binary_mask(label_7)
    convert_multiclass_to_binary_mask(label_8)
    convert_multiclass_to_binary_mask(label_9)
    convert_multiclass_to_binary_mask(label_10)
    convert_multiclass_to_binary_mask(label_11)

    """Create stack & encoded array"""
    label_list = [label_0, label_1, label_2, label_3, label_4,
                  label_5, label_6, label_7, label_8, label_9, label_10, label_11]
    for i in range(1, len(label_list)):
        label_0[label_list[i] == 1] = 0

    output = np.stack(label_list, axis=-1)
    np.save("./output/correct_mask.npy", output)


if __name__ == "__main__":
    """
    if class does not exist in prediction -> intersecton = 0 -> nominator = smooth 
    if prediction also does not have class -> smooth / smooth = 1
    if prediction has that class -> smooth / reduce_sum(pred) + smooth = a very small number
    """
    # truth = np.array([1, 2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    # prediction = np.array([1, 2, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4])
    # correct = np.array([1, 2, 3])

    # print(dice_score(truth, prediction, 4))

    triple_view = np.load("./output/intersection_encode.npy").astype(np.uint8)
    # axial = np.load("./output/axial_encode.npy")
    # saggital = np.load("./output/saggital_encode.npy")
    # coronal = np.load("./output/coronal_encode.npy")

    # save_whole_mask("E:\\ISEF\\VHSCDD\\VHSCDD labels\\VHSCDD_020_label")
    ground_truth = np.load("./output/correct_mask.npy").astype(np.uint8)

    # print(f"Triple View: {dice_coef(ground_truth, triple_view)} || Axial: {dice_coef(ground_truth, axial)} || Saggital: {dice_coef(ground_truth, saggital)} || Coronal: {dice_coef(ground_truth, coronal)}")

    print(dice_coef_numpy(ground_truth, triple_view))
