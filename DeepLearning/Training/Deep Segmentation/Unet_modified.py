import os
import tensorflow as tf
os.environ["tf_gpu_allocator"] = "cuda_malloc_async"


def CreateUnetModified(num_classes, x, y, z):
    # Build the model
    inputs = tf.keras.layers.Input(shape=(x, y, z, 1))
    s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

    # Contraction path (Encoder)

    # First layer
    c1 = tf.keras.layers.Conv3D(16,
                                (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
    # c1 = tf.keras.layers.Conv3D(16, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c1)
    d1 = tf.keras.layers.Conv3D(
        32, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(c1)

    # Second layer
    c2 = tf.keras.layers.Conv3D(32, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(d1)
    # c2 = tf.keras.layers.Conv3D(32, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c2)

    d2 = tf.keras.layers.Conv3D(
        64, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(c2)

    # Third layer
    c3 = tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(d2)
    # c3 = tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c3)
    d3 = tf.keras.layers.Conv3D(
        128, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(c3)

    # Fourth layer
    c4 = tf.keras.layers.Conv3D(128, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(d3)
    # c4 = tf.keras.layers.Conv3D(128, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c4)
    d4 = tf.keras.layers.Conv3D(
        256, (2, 2, 2), strides=(2, 2, 2), activation="relu", kernel_initializer="he_normal", padding="same")(c4)

    # Fifth layer
    c5 = tf.keras.layers.Conv3D(256, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(d4)
    # c5 = tf.keras.layers.Conv3D(256, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c5)

    # Expansive path (Decoder)
    u5 = tf.keras.layers.Conv3DTranspose(
        256, (2, 2, 2), strides=(2, 2, 2), padding="same")(c5)
    c6 = tf.keras.layers.Concatenate()([u5, c4])
    c6 = tf.keras.layers.Conv3D(256, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c6)
    # c6 = tf.keras.layers.Conv3D(256, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c6)
    u6 = tf.keras.layers.Conv3DTranspose(
        128, (2, 2, 2), strides=(2, 2, 2), padding="same")(c6)

    c7 = tf.keras.layers.Concatenate()([u6, c3])
    c7 = tf.keras.layers.Conv3D(128, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c7)
    # c7 = tf.keras.layers.Conv3D(128, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c7)
    u7 = tf.keras.layers.Conv3DTranspose(
        64, (2, 2, 2), strides=(2, 2, 2), padding="same")(c7)

    c8 = tf.keras.layers.Concatenate()([u7, c2])
    c8 = tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    # c8 = tf.keras.layers.Conv3D(64, (3, 3, 3), activation='relu',
    #                             kernel_initializer='he_normal', padding='same')(c8)
    u8 = tf.keras.layers.Conv3DTranspose(
        32, (2, 2, 2), strides=(2, 2, 2), padding="same")(c8)

    c9 = tf.keras.layers.Concatenate()([u8, c1])
    c9 = tf.keras.layers.Conv3D(32, (3, 3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c9)

    outputs = tf.keras.layers.Conv3D(
        num_classes, (1, 1, 1), activation='softmax')(c9)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

