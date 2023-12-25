import os
import skimage.transform as skTrans
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import math
import multiprocessing
path = "E:\\ISEF\\ImageCHD//ImageCHD_dataset"
save_path = "E:\\ISEF\\ImageCHD\\ImageCHD_dataset_resize"


def OneHotEncodeVHSCDD(label_input_path, x_: int, y_: int, z_: int, save_path):
    """
    Create a one hot encode + resized version of original array without the need for color interpolation or external libraries
    arguments: 
        orginal: original, unresized array
        x_: prefered x size for new array 
        y_: prefered y size for new array 
        z_: prefered z size for new array 
        num_classes: number of unique elements inside array 
    """

    original = nib.load(label_input_path).get_fdata()
    print(f"one hot encode: {original.shape}")

    num_classes = len(np.unique(original))

    def GenerateEncodeList(num_classes):
        encodeList = {}
        unique_element = np.unique(original)

        if len(unique_element) != num_classes:
            num_classes = len(unique_element)

        unique_elem_counter = 0
        for elem in unique_element:
            encodeList[elem] = unique_elem_counter
            unique_elem_counter += 1

        return encodeList

    encodeList = GenerateEncodeList(num_classes)
    print(encodeList)

    x, y, z = original.shape

    labelEncode = np.empty((x_, y_, z_, num_classes), dtype="uint8")
    for i_ in range(x_):
        for j_ in range(y_):
            for k_ in range(z_):
                i = math.floor((i_ * x) / x_)
                j = math.floor((j_ * y) / y_)
                k = math.floor((k_ * z) / z_)

                i = max(0, min(i, x - 1))
                j = max(0, min(j, y - 1))
                k = max(0, min(k, z - 1))

                value = original[i][j][k]

                encodeIndex = encodeList[value]

                for n in range(num_classes):
                    labelEncode[i_][j_][k_][n] = 0

                labelEncode[i_][j_][k_][encodeIndex] = 1

    np.save(save_path, labelEncode)
    del labelEncode


def WorkerImageReshapeFunction(input_path, save_path):
    img = nib.load(input_path)
    print(f"Worker shape: {img.shape}")
    data = img.get_fdata()
    resize_data = np.array(skTrans.resize(data, (512, 600, 600), order=1,
                                          preserve_range=True, anti_aliasing=True), dtype="float16")
    np.save(save_path, resize_data)
    del resize_data


def RenameBrokenFile(root_dir_path):
    for file in os.listdir(root_dir_path):
        old_path = os.path.join(root_dir_path, file)
        splitted = old_path.split("_")
        ordering = int(splitted[-1].split(".")[0])
        ordering -= 7
        new_path = "_".join(
            splitted[0:len(splitted) - 1:1]) + f"_final_{ordering}.npy"
        print(f"Old: {old_path} || New: {new_path}")
        os.rename(old_path, new_path)


if __name__ == "__main__":
    label_ordering = 1
    image_ordering = 1

    path_list = os.listdir(path)
    path_list = path_list[156::1]
    for file in path_list:
        print(file)
        extension = file.split("_")[-1].split(".")
        if extension[0] == "label":
            # create path
            label_save_path = f"{save_path}//label__final_{label_ordering}.npy"
            label_ordering += 1
            label_input_path = os.path.join(path, file)

            # add process to list
            OneHotEncodeVHSCDD(label_input_path, 512, 600,
                               600, label_save_path)

        else:
            image_save_path = f"{save_path}//image_final_{image_ordering}.npy"
            image_ordering += 1
            image_input_path = os.path.join(path, file)

            WorkerImageReshapeFunction(image_input_path, image_save_path)
