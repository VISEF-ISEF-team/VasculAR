import warnings
warnings.filterwarnings('ignore')
import cv2
import numpy as np
from keras import backend as K

import SimpleITK as sitk

def dice_coefficient(y_true, y_pred, smooth=1):
    """
    Computes the Dice coefficient, a statistical metric used for comparing the similarity 
    of two samples. It is especially used for comparing the pixel-wise agreement between a 
    predicted segmentation and its corresponding ground truth.

    The Dice coefficient is defined as 2 * |X ∩ Y| / (|X|+|Y|), where X is the true mask 
    of an image and Y is the predicted mask. In other words, it's twice the area of overlap 
    between the predicted and ground truth, divided by the total number of pixels in both 
    images. 

    Parameters:
    -----------
    y_true : array
        The ground truth masks.
    
    y_pred : array
        The predicted masks.

    smooth : float, optional (default is 1)
        A smoothing factor to prevent division by zero in case there's no overlap between 
        the predicted and ground truth masks.

    Returns:
    --------
    float
        The Dice coefficient, a float between 0 (complete dissimilarity) and 1 (complete similarity).
    """
    intersection = K.sum(y_true * y_pred, axis=[1, 2, 3])
    union = K.sum(y_true, axis=[1, 2, 3]) + K.sum(y_pred, axis=[1, 2, 3])
    return K.mean((2. * intersection + smooth) / (union + smooth), axis=0)


# y_pred = cv2.imread('image_1.png')/255.
# y_true = cv2.imread('image_2.png')/255.

# print(y_pred.shape)
# print(y_true.shape)

# y_pred = y_pred.reshape((-1, 853, 640, 3 ))
# y_true = y_true.reshape((-1, 853, 640, 3 ))

# print(y_pred.shape)
# print(y_true.shape)


ground_truth = sitk.ReadImage("ct_train_1001_label.nii.gz", sitk.sitkFloat32)
ground_truth = sitk.GetArrayFromImage(ground_truth)

prediction = sitk.ReadImage("ct_train_1001_predicted.nii.gz", sitk.sitkFloat32)
prediction = sitk.GetArrayFromImage(prediction)

print(ground_truth.shape, prediction.shape)