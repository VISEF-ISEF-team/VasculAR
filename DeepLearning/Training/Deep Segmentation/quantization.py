import numpy as np
from keras import backend as K
import numpy as np
from unet_attention import Attention_Unet
import tensorflow as tf
from metrics import dice_coef, dice_loss


if __name__ == "__main__":
    input_shape = (600, 512, 1)
    model_path = "C:\\Users\\Acer\\OneDrive\\Documents\\Model Data\\coronal_dice-loss_model_normal.h5"

    K.set_floatx("float32")
    model = tf.keras.models.load_model(model_path, custom_objects={
                                       "dice_loss": dice_loss, "dice_coef": dice_coef})

    K.set_floatx("float16")
    ws = model.get_weights()
    wsp = [w.astype(K.floatx()) for w in ws]

    # all weights are now float 16
    print(np.unique([w.dtype for w in wsp]))
    model_quant = Attention_Unet(input_shape, 12)
    model_quant.set_weights(wsp)

    for layer in model_quant.layers:
        layer.set_weights([w.astype(np.float16) for w in layer.get_weights()])

    print(np.unique([w.dtype for w in model.get_weights()]))
    print(np.unique([w.dtype for w in model_quant.get_weights()]))

    model_quant.compile(loss=dice_loss, optimizer=tf.keras.optimizers.Adam(
        1e-4), metrics=[dice_coef, "accuracy"])
    model_quant.save("./Optimized Model and Graph/coronal.h5")
