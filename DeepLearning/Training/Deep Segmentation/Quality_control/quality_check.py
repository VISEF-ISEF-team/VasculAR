import os
import numpy as np
from glob import glob
import nibabel as nib
import re
import time


def extract_label_number(path):
    # Extract the label number from the file name using regular expression
    match = re.search(r'ct_\d+_label_(\d+)\.nii', path)
    if match:
        return int(match.group(1))
    else:
        return -1  # Return -1 if no label number is found


def check(folder):
    separate_mask_path = sorted(
        glob(os.path.join(folder, "output", "*.nii")), key=extract_label_number)

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
    label_list = [label_1, label_2, label_3, label_4,
                  label_5, label_6, label_7, label_8, label_9, label_10, label_11]

    print(folder)
    for label in label_list:
        print(label.shape)
    print("-------------------------------------------------------------------------------------------------------")
    print()


if __name__ == "__main__":
    root = "E:\ISEF\VHSCDD\VHSCDD labels separated"

    for folder in sorted(glob(os.path.join(root, "*"))):
        check(folder)

    # 30

    # check("E:\ISEF\VHSCDD\VHSCDD labels separated\VHSCDD_041_label")
