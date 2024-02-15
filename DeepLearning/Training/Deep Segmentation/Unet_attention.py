import tensorflow as tf
from tensorflow.keras.models import Model
import tensorflow.keras.layers as L


def conv_block(x, num_filters):
    x = L.Conv2D(num_filters, 3, padding="same")(x)
    x = L.BatchNormalization()(x)
    x = L.Activation("relu")(x)

    x = L.Conv2D(num_filters, 3, padding="same")(x)
    x = L.BatchNormalization()(x)
    x = L.Activation("relu")(x)

    return x


def encoder_block(x, num_filters):
    x = conv_block(x, num_filters)
    p = L.MaxPooling2D((2, 2))(x)
    return x, p


def attention_gate(g, s, num_filters):
    Wg = L.Conv2D(num_filters, 1, padding="same")(g)
    Wg = L.BatchNormalization()(Wg)

    Ws = L.Conv2D(num_filters, 1, padding="same")(s)
    Ws = L.BatchNormalization()(Ws)

    output = L.Activation("relu")(Wg + Ws)
    output = L.Conv2D(num_filters, 1, padding="same")(output)
    output = L.Activation("sigmoid")(output)

    return output * s


def decoder_block(x, s, num_filters):
    x = L.UpSampling2D(interpolation="bilinear")(x)
    s = attention_gate(x, s, num_filters)
    x = L.Concatenate()([x, s])
    x = conv_block(x, num_filters)
    return x


def Attention_Unet(input_shape, num_classes):
    inputs = L.Input(input_shape)

    """Encoder"""
    s1, p1 = encoder_block(inputs, 64)
    s2, p2 = encoder_block(p1, 128)
    s3, p3 = encoder_block(p2, 256)

    b1 = conv_block(p3, 512)

    """Decoder"""
    d1 = decoder_block(b1, s3, 256)
    d2 = decoder_block(d1, s2, 128)
    d3 = decoder_block(d2, s1, 64)

    """Output"""
    outputs = L.Conv2D(num_classes, 1, padding="same",
                       activation="softmax")(d3)

    """Model"""
    model = Model(inputs, outputs, name="Attention-UNet")
    return model
