'''
Full pipeline
- PAT001
    - dcm001.dcm
    - ...
    - dcm201.dcm
- PAT01_mask_01
    - dcm001.png
    - ...
    - dcm201.png
- ...
- PAT034
'''

import numpy as np
from pydicom import dcmread
import scipy.ndimage
import os
import glob
import imageio
import numpy as np
from PIL import Image
import nibabel as nib
import SimpleITK as sitk
from vis import *


def convert_mask(in_path, out_path):
    # Get a list of all the png files in the folder
    png_files = glob.glob(in_path)

    # Read each file as a numpy array and append to a list
    img_list = []
    for file in png_files:
        img = imageio.imread(file)
        img_list.append(img)

    # Stack the arrays along the z-axis
    img_3d = np.stack(img_list, axis=0)

    # Define a function to convert a single RGB image to grayscale
    def rgb2gray(rgb_img):
        return np.dot(rgb_img[...,:3], [0.2989, 0.5870, 0.1140])

    # Apply the function to each image along the z-axis
    gray_3d = np.apply_along_axis(rgb2gray, axis=3, arr=img_3d)
    print(gray_3d.shape)


    # Create a nibabel object from the array and save it as a file
    converted_array = np.array(gray_3d, dtype=np.float32)
    converted_array = np.transpose(converted_array, (1, 2, 0))

    affine = np.eye(4)
    nifti_file = nib.Nifti1Image(converted_array, affine)
    nib.save(nifti_file, out_path)

    # reread to check
    raw_img_sitk = sitk.ReadImage(out_path, sitk.sitkFloat32)
    raw_img_sitk = sitk.GetArrayFromImage(raw_img_sitk)
    print(f'Shape of numpy array: {raw_img_sitk.shape}')


# Create .nii.gz for all masks for all patients
def all_patients():
    for i in range(1,2):
        if i < 10:
            i = "0" + str(i) 
        for j in range(1,3):
            convert_mask(in_path=f"PAT0{i}_mask_{j}/*.png", out_path=f"res/PAT0{i}_mask_{j}.nii.gz")
            
def one_patient():
    for j in range(1,3):
        convert_mask(in_path=f"PAT0035_mask_{j}/*.png", out_path=f"res/PAT0035_mask_{j}.nii.gz")

# 3D vizualization on the new patient
run()