import tensorflow as tf
from tensorflow.keras import layers


def conv(in_ch, out_ch, num):
    conv_list = []
    for _ in range(num - 1):
        conv_list.extend([
            layers.Conv2D(out_ch, 3, padding='same',
                          kernel_initializer='glorot_uniform'),
            layers.BatchNormalization(),
            layers.ReLU()
        ])

    return tf.keras.Sequential([
        layers.Conv2D(out_ch, 3, padding='same',
                      kernel_initializer='glorot_uniform'),
        layers.BatchNormalization(),
        layers.ReLU()
    ] + conv_list)


class FCN8s(tf.keras.Model):
    def __init__(self, n_class, input_shape):
        super(FCN8s, self).__init__()

        self.conv1 = conv(3, 64, 2)
        self.pool1 = layers.MaxPooling2D(pool_size=2, strides=2)

        self.conv2 = conv(64, 128, 2)
        self.pool2 = layers.MaxPooling2D(pool_size=2, strides=2)

        self.conv3 = conv(128, 256, 3)
        self.pool3 = layers.MaxPooling2D(pool_size=2, strides=2)

        self.conv4 = conv(256, 512, 3)
        self.pool4 = layers.MaxPooling2D(pool_size=2, strides=2)

        self.conv5 = conv(512, 512, 3)
        self.pool5 = layers.MaxPooling2D(pool_size=2, strides=2)

        self.conv6 = tf.keras.Sequential([
            layers.Conv2D(4096, 7, kernel_initializer='glorot_uniform'),
            layers.BatchNormalization(),
            layers.ReLU(),
        ])

        self.conv7 = tf.keras.Sequential([
            layers.Conv2D(4096, 1, kernel_initializer='glorot_uniform'),
            layers.BatchNormalization(),
            layers.ReLU(),
        ])

        self.score_fr = layers.Conv2D(
            n_class, 1, kernel_initializer='glorot_uniform')

        self.upscore2 = layers.Conv2DTranspose(
            n_class, 4, strides=2, padding='same', kernel_initializer='glorot_uniform')

        self.score_pool4 = layers.Conv2D(
            n_class, 1, kernel_initializer='glorot_uniform')

        self.upscore_pool4 = layers.Conv2DTranspose(
            n_class, 4, strides=2, padding='same', kernel_initializer='glorot_uniform')

        self.score_pool3 = layers.Conv2D(
            n_class, 1, kernel_initializer='glorot_uniform')

        self.upscore8 = layers.Conv2DTranspose(
            n_class, 16, strides=8, padding='same', kernel_initializer='glorot_uniform')

        self.output_layer = layers.Conv2D(
            n_class, 1, activation='softmax', kernel_initializer='glorot_uniform')

    def call(self, x):
        x1 = self.conv1(x)
        p1 = self.pool1(x1)
        x2 = self.conv2(p1)
        p2 = self.pool2(x2)
        x3 = self.conv3(p2)
        p3 = self.pool3(x3)
        x4 = self.conv4(p3)
        p4 = self.pool4(x4)
        x5 = self.conv5(p4)
        p5 = self.pool5(x5)

        x6 = self.conv6(p5)
        x7 = self.conv7(x6)

        sf = self.score_fr(x7)
        u2 = self.upscore2(sf)

        s4 = self.score_pool4(p4)
        f4 = tf.add(s4, u2)
        u4 = self.upscore_pool4(f4)

        s3 = self.score_pool3(p3)
        f3 = tf.add(s3, u4)
        upscored = self.upscore8(f3)

        return self.output_layer(upscored)

    def build(self, input_shape):
        # Explicitly call the build method for each layer
        self.conv1.build(input_shape)
        self.pool1.build(input_shape)
        self.conv2.build(input_shape)
        self.pool2.build(input_shape)
        self.conv3.build(input_shape)
        self.pool3.build(input_shape)
        self.conv4.build(input_shape)
        self.pool4.build(input_shape)
        self.conv5.build(input_shape)
        self.pool5.build(input_shape)
        self.conv6.build(input_shape)
        self.conv7.build(input_shape)
        self.score_fr.build(input_shape)
        self.upscore2.build(input_shape)
        self.score_pool4.build(input_shape)
        self.upscore_pool4.build(input_shape)
        self.score_pool3.build(input_shape)
        self.upscore8.build(input_shape)
        self.output_layer.build(input_shape)
        super(FCN8s, self).build(input_shape)


# Example usage:
num_classes = 8
input_shape = (512, 512, 1)  # Replace with the actual input shape of your data
fcn8s_model = FCN8s(num_classes, input_shape)

# Explicitly build the model
fcn8s_model.build(input_shape=(None, *input_shape))

# Print the model summary
fcn8s_model.summary()

# Calculate and print the total number of parameters
total_params = fcn8s_model.count_params()
print("Total number of parameters:", total_params)

# Compile the model
fcn8s_model.compile(
    optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
