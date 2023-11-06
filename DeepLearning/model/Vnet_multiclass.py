import tensorflow as tf
import numpy as np
import os
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


def FillWithBone(image: np.array, label: np.array, target: int):
    """Fill slices to the shape requirement by taking the last slice and duplicating it if it's only 0. Else we fill with black color.
    Returns 2 new array with the number of slices equals to target.
    """

    x, y, z = label.shape

    if label.shape[-1] == target:
        return image, label
    else:
        uniqueValue = np.unique(label[:, :, -1])
        if len(uniqueValue) <= 1 and uniqueValue[0] == 0:

            # append zeros to the
            newLabel = np.append(label, np.zeros(
                (x, y, target - z), dtype="uint8"), axis=2)

            # copy last slices of image to append to
            newImage = []
            for _ in range(target - z):
                newImage.append(image[:, :, -1])
            newImage = np.append(image, newImage, axis=2)

            return newImage, newLabel

        else:
            # If the last slice does also contain heart, fill both image and label with zero to represent dark background
            newImage = np.append(label, np.zeros((x, y, target - z)), axis=2)
            newLabel = np.append(image, np.zeros((x, y, target - z)), axis=2)

            return newImage, newLabel


