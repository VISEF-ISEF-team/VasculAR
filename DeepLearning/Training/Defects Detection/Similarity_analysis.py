import numpy as np
import os
import matplotlib.pyplot as plt
import nibabel as nib
import SimpleITK as sitk
import skimage.transform as skTrans

structure_1_path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD/VHSCDD_013_label/ct_0013_label_7.nii.gz"
structure_2_path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD/VHSCDD_019_label/ct_0039_label_7.nii.gz"
structure_3_path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD/VHSCDD_014_label/ct_0088_label_7.nii.gz"

def dice_coefficient(array1, array2):
    intersection = np.sum(array1 * array2)
    union = np.sum(array1) + np.sum(array2)
    return 2.0 * intersection / union if union > 0 else 1.0

def jaccard_index(array1, array2):
    intersection = np.sum(array1 * array2)
    union = np.sum(np.logical_or(array1, array2))
    return intersection / union if union > 0 else 1.0

structure_1 = sitk.ReadImage(structure_1_path, sitk.sitkFloat32)
structure_1 = sitk.GetArrayFromImage(structure_1)

structure_2 = sitk.ReadImage(structure_2_path, sitk.sitkFloat32)
structure_2 = sitk.GetArrayFromImage(structure_2)

structure_3 = sitk.ReadImage(structure_3_path, sitk.sitkFloat32)
structure_3 = sitk.GetArrayFromImage(structure_3)

print(
    dice_coefficient(structure_1, structure_2),
    dice_coefficient(structure_2, structure_3),
    dice_coefficient(structure_1, structure_3),
)

print(
    jaccard_index(structure_1, structure_2),
    jaccard_index(structure_2, structure_3),
    jaccard_index(structure_1, structure_3),
)