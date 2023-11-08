import tensorflow as tf
import numpy as np
import os
import math
import nibabel as nib
import skimage.transform as skTrans


def OneHotEncode(original: np.array, x_: int, y_: int, z_: int, num_classes=8):
    """
    Create a one hot encode + resized version of original array without the need for color interpolation or external libraries
    arguments: 
        orginal: original, unresized array
        x_: prefered x size for new array 
        y_: prefered y size for new array 
        z_: prefered z size for new array 
    """
    encodeList = {
        0: 0,
        500: 1,
        600: 2,
        420: 3,
        550: 4,
        205: 5,
        820: 6,
        850: 7,
    }

    x, y, z = original.shape

    labelEncode = np.empty((x_, y_, z_, num_classes), dtype="float16")
    for i_ in range(x_):
        for j_ in range(y_):
            for k_ in range(z_):
                i = math.floor((i_ * x) / x_)
                j = math.floor((j_ * y) / y_)
                k = math.floor((k_ * z) / z_)

                i = max(0, min(i, x - 1))
                j = max(0, min(j, y - 1))
                k = max(0, min(k, k - 1))

                value = original[i][j][k]

                encodeIndex = encodeList[value]

                for n in range(8):
                    labelEncode[i_][j_][k_][n] = 0

                labelEncode[i_][j_][k_][encodeIndex] = 1

    return labelEncode


def GenerateEncodeData(rootDirPath, pathList, x_, y_, z_):
    """Create and save encoded lable to reduce training time"""
    newDirPath = "..\\mmwhs\\ct_label_encode\\"
    ordering = 0

    def GetType(fullPath):
        return fullPath.split("_")[-1].split(".")[0] == "label"

    for path in pathList:
        fullPath = os.path.join(rootDirPath, path)
        if GetType(fullPath):
            original = np.array(
                nib.load(fullPath).get_fdata(), dtype="float16")
            labelEncode = OneHotEncode(original, x_, y_, z_)
            print(labelEncode.shape)
            np.save(os.path.join(
                newDirPath, f"encode_{ordering}"), labelEncode)
            ordering += 1


def GenerateData(start: int, stop: int, pathList: list, rootDirPath: str):
    """
    Generate and resized image + generated resized encoded label for training
    arguments: 
        start: start index in pathList
        stop: stop index in pathList
        pathList: list containing paths of all files that is in the directory of rootDirPath so that they can be concatenated together
        rootDirPath: path to the root directory containing all training files, in this case, it's the "mmwhs//ct_train//" path

        This function works when image and label are in the same folder with alternating order.
    """
    # target is 368 to allow Vnet to compress and decompress
    X = []
    Y = []
    for i in range(start, stop, 2):
        imagePath = os.path.join(rootDirPath, pathList[i])
        labelPath = os.path.join(rootDirPath, pathList[i + 1])

        image = np.array(nib.load(imagePath).get_fdata(), dtype="float16")
        label = np.array(nib.load(labelPath).get_fdata(), dtype="int8")

        image = skTrans.resize(image, (128, 128, 256),
                               order=1, preserve_range=True)

        label = OneHotEncode(label, 128, 128, 256)

        image = np.expand_dims(image, -1)

        print(f"Image shape: {image.shape} || Path: {imagePath}")
        print(f"Label shape : {label.shape} || Path: {labelPath}")

        X.append(image)
        Y.append(label)

    X = np.array(X)
    Y = np.array(Y)

    del image
    del label
    del imagePath
    del labelPath

    return X, Y


def TrainingLoop(model, pathList):
    for i in range(0, 30, 2):
        X, Y = GenerateData(i, i + 2, pathList)
        model.fit(X, Y, epochs=1, verbose=1)
        del X
        del Y


def GenerateDataWithEncode(start, stop, encodePath, rootDirPath, encodeIndex):
    X = []
    Y = []
    pathList = os.listdir(rootDirPath)
    encodeList = os.listdir(encodePath)

    def SortEncodeKey(filename):
        return int(filename.split('_')[1].split('.')[0])

    def SortImageKey(filename):
        parts = filename.split('_')
        return (int(parts[2]), parts[3])

    # sort path and image
    pathList = sorted(pathList, key=SortImageKey)
    encodeList = sorted(encodeList, key=SortEncodeKey)

    for i in range(start, stop, 2):
        imagePath = os.path.join(rootDirPath, pathList[i])

        image = np.array(nib.load(imagePath).get_fdata(), dtype="float16")
        image = skTrans.resize(image, (256, 256, 256),
                               order=1, preserve_range=True)
        image = np.expand_dims(image, -1)

        labelPath = os.path.join(encodePath, encodeList[encodeIndex])
        label = np.load(labelPath)

        print(f"Image shape: {image.shape} || Path: {imagePath}")
        print(f"Label shape : {label.shape} || Path: {labelPath}")

        X.append(image)
        Y.append(label)

    X = np.array(X)
    Y = np.array(Y)
    return X, Y


def TrainingLoopWithEncode(model, encodePath, rootDirPath):
    encodeIndex = 0
    initialEpoch = 0
    for i in range(0, 30, 2):
        X, Y = GenerateDataWithEncode(
            i, i + 2, encodePath, rootDirPath, encodeIndex)
        model.fit(X, Y, epochs=1, verbose=1, initial_epoch=initialEpoch)
        del X
        del Y
        encodeIndex += 1
        initialEpoch += 1


if __name__ == "__main__":
    rootDirPath = "..\\mmwhs\\ct_train"
    pathList = os.listdir(rootDirPath)
    GenerateEncodeData(rootDirPath, pathList, 256, 256, 256)
