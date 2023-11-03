import tensorflow as tf


def CreateVnet(x, y, z):

    # Build the model
    inputs = tf.keras.layers.Input((x, y, z))
    # normalize the pixel to floating point
    s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

    # Contraction path (Encoder)

    # First layer
    c1 = tf.keras.layers.Conv3D(16,
                                (5, 5, 5), activation='relu', kernel_initializer='he_normal', padding='same')(s),
    c1 = tf.keras.layers.Conv3D(16, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c1)
    a1 = tf.keras.layers.Add()([c1, s])
    d1 = tf.keras.layers.Conv3D(
        16, (2, 2, 2), stride=2, activation="relu", kernel_initializer="he_normal")(a1)
    p1 = tf.keras.layers.PReLU()(d1)

    # Second layer
    c2 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p1)
    c2 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c2)

    a2 = tf.keras.layers.Add()[c2, p1]
    d2 = tf.keras.layers.Conv3D(
        32, (2, 2, 2), stride=2, activation="relu", kernel_initializer="he_normal")(a2)
    p2 = tf.keras.layers.PReLU()(d2)

    # Third layer
    c3 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p2)
    c3 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c3)
    a3 = tf.keras.layers.Add()[c3, p2]
    d3 = tf.keras.layers.Conv3D(
        64, (2, 2, 2), stride=2, activation="relu", kernel_initializer="he_normal")(a3)
    p3 = tf.keras.layers.PreLU()(d3)

    # Fourth layer
    c4 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p3)
    c4 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c4)
    a4 = tf.keras.layers.Add()[c4, p3]
    d4 = tf.keras.layers.Conv3D(
        128, (2, 2, 2), stride=2, activation="relu", kernel_initializer="he_normal")(a4)
    p4 = tf.keras.layers.PreLU()(d4)

    # Fifth layer
    c5 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(p4)
    c5 = tf.keras.layers.Conv3D(256, (3, 3), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c5)
    a5 = tf.keras.layers.Add()[c5, p4]

    # Expansive path (Decoder)
    u5 = tf.keras.layers.Conv3DTranspose(
        256, (2, 2, 2), strides=2, padding='same')(a5)
    p5 = tf.keras.layers.PreLU()(u5)
    c6 = tf.keras.layers.concatenate([p5, a4])
    c6 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c6)
    c6 = tf.keras.layers.Conv3D(256, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c6)
    a6 = tf.keras.layers.Add()[p5, c6]
    u6 = tf.keras.layers.Conv3DTranspose(256, (2, 2, 2), strides=2, padding="same")(a6)
    p6 = tf.keras.layers.PreLU()(u6)

    c7 = tf.keras.layers.concatenate([p6, a3])
    c7 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c7)
    c7 = tf.keras.layers.Conv3D(128, (5, 5, 5), activation='relu',
                            kernel_initializer='he_normal', padding='same')(c7)
    a7 = tf.keras.layers.Add()[p6, c7]
    u7 = tf.keras.layers.Conv3DTranspose(128, (2, 2, 2), strides=2, padding="same")(a7)
    p7 = tf.keras.layers.PreLU()(u7)

    c8 = tf.keras.layers.concatenate([p7, a2])
    c8 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    c8 = tf.keras.layers.Conv3D(64, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    a8 = tf.keras.layers.Add()[p7, c8]
    u8 = tf.keras.layers.Conv3DTranspose(64, (2, 2, 2), strides=2, padding="same")(a8)
    p8 = tf.keras.layers.PreLU()(u8)

    c9 = tf.keras.layers.concatenate([p8, a1])
    c9 = tf.keras.layers.Conv3D(32, (5, 5, 5), activation='relu',
                                kernel_initializer='he_normal', padding='same')(c8)
    a9 = tf.keras.layers.Add()[p8, c9]
    outputs = tf.keras.layers.Conv3D(1, (1, 1, 1), activation='sigmoid')(c9)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    # Modelcheckpoint
    checkpointer = tf.keras.callbacks.ModelCheckpoint(
        'cardiac_segmentation_model.h5', verbose=1, save_best_only=True)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'),
        tf.keras.callbacks.TensorBoard(log_dir='logs')
    ]

    # results = model.fit(X_train, Y_train, validation_split=0.1, batch_size=16, epochs=25, callbacks=callbacks)
