import tensorflow as tf
import numpy as np
import os
import math
import nibabel as nib
import skimage.transform as skTrans
os.environ["tf_gpu_allocator"] = "cuda_malloc_async"


def CreateVnet():

    # Build the model
    inputs = tf.keras.layers.Input(shape=(512, 512, 384, 1))
    # normalize the pixel to floating point
    # s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

    # Contraction path (Encoder)

    # First layer
    c1 = tf.keras.layers.Conv3D(16,
                                (5, 5, 5), activation='relu', kernel_initializer='he_normal', padding='same')(inputs)
    c1 = tf.keras.layers.Conv3D(16, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c1)
    a1 = tf.keras.layers.Add()([c1, inputs])
    d1 = tf.keras.layers.Conv3D(
        32, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(a1)
    p1 = tf.keras.layers.PReLU()(d1)

    # Second layer
    c2 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p1)
    c2 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c2)

    a2 = tf.keras.layers.Add()([c2, p1])
    d2 = tf.keras.layers.Conv3D(
        64, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(a2)
    p2 = tf.keras.layers.PReLU()(d2)

    # Third layer
    c3 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p2)
    c3 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c3)
    a3 = tf.keras.layers.Add()([c3, p2])
    d3 = tf.keras.layers.Conv3D(
        128, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(a3)
    p3 = tf.keras.layers.PReLU()(d3)

    # Fourth layer
    c4 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p3)
    c4 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c4)
    a4 = tf.keras.layers.Add()([c4, p3])
    d4 = tf.keras.layers.Conv3D(
        256, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(a4)
    p4 = tf.keras.layers.PReLU()(d4)

    # Fifth layer
    c5 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p4)
    c5 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c5)
    a5 = tf.keras.layers.Add()([c5, p4])

    # Expansive path (Decoder)
    u5 = tf.keras.layers.Conv3DTranspose(
        256, (2, 2, 2), strides=(2, 2, 2), padding="same")(a5)
    p5 = tf.keras.layers.PReLU()(u5)
    c6 = tf.keras.layers.Concatenate()([p5, a4])
    c6 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c6)
    c6 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c6)
    a6 = tf.keras.layers.Add()([p5, c6])
    u6 = tf.keras.layers.Conv3DTranspose(
        128, (2, 2, 2), strides=(2, 2, 2), padding="same")(a6)
    p6 = tf.keras.layers.PReLU()(u6)

    c7 = tf.keras.layers.Concatenate()([p6, a3])
    c7 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c7)
    c7 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c7)
    a7 = tf.keras.layers.Add()([p6, c7])
    u7 = tf.keras.layers.Conv3DTranspose(
        64, (2, 2, 2), strides=(2, 2, 2), padding="same")(a7)
    p7 = tf.keras.layers.PReLU()(u7)

    c8 = tf.keras.layers.Concatenate()([p7, a2])
    c8 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    c8 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    a8 = tf.keras.layers.Add()([p7, c8])
    u8 = tf.keras.layers.Conv3DTranspose(
        32, (2, 2, 2), strides=(2, 2, 2), padding="same")(a8)
    p8 = tf.keras.layers.PReLU()(u8)

    c9 = tf.keras.layers.Concatenate()([p8, a1])
    c9 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c9)
    a9 = tf.keras.layers.Add()([p8, c9])

    outputs = tf.keras.layers.Conv3D(
        1, (1, 1, 1), activation='softmax', padding="same")(a9)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # results = model.fit(X_train, Y_train, validation_split=0.1, batch_size=16, epochs=25, callbacks=callbacks)
    model.save(".\\vnet.keras")


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

                encodeIndex = encodeList[value] = 1

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
