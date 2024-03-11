import tensorflow as tf
from tensorflow import keras
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
from tensorflow.keras.utils import CustomObjectScope
import numpy as np
from metrics import dice_coef, dice_loss
# path of the directory where you want to save your model
frozen_out_path = "./Optimized Model and Graph/"
# name of the .pb file
frozen_graph_filename = "coronal_frozen_graph"


def save_frozen_graph():
    model = tf.keras.models.load_model(
        "./Optimized Model and Graph/coronal.h5", custom_objects={"dice_coef": dice_coef, "dice_loss": dice_loss})
    # Convert Keras model to ConcreteFunction
    full_model = tf.function(lambda x: model(x))
    full_model = full_model.get_concrete_function(
        tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))
    # Get frozen ConcreteFunction

    frozen_func = convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()
    layers = [op.name for op in frozen_func.graph.get_operations()]
    print("-" * 60)
    print("Frozen model layers: ")
    for layer in layers:
        print(layer)
    print("-" * 60)
    print("Frozen model inputs: ")
    print(frozen_func.inputs)
    print("Frozen model outputs: ")
    print(frozen_func.outputs)
    # Save frozen graph to disk
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir=frozen_out_path,
                      name=f"{frozen_graph_filename}.pb",
                      as_text=False)

    # Save its text representation
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir=frozen_out_path,
                      name=f"{frozen_graph_filename}.pbtxt",
                      as_text=True)


if __name__ == "__main__":
    save_frozen_graph()


# python -m tensorflow.python.tools.optimize_for_inference --input ./model_20K_96_soft_f1/frozen_model/frozen_graph.pb --output ./model_20K_96_soft_f1/optimized/optmized_graph.pb --frozen_graph=True --input_names=x --output_names=Identity
