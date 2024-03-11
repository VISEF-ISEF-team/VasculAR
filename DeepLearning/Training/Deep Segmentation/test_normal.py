from train import load_dataset, read_image, read_mask, specific_case_load_dataset
from metrics import dice_loss, dice_coef, dice_score, dice_score_per_class
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, jaccard_score, precision_score, recall_score
from tensorflow.keras.utils import CustomObjectScope
from tqdm import tqdm
from glob import glob
import pandas as pd
import cv2
import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tfc
import os
from train import load_dataset, tf_dataset
import matplotlib.pyplot as plt
import time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

"""HypearParameters"""
global VIEW


def test_model_with_dice_in_training(x_test, y_test, model_path):
    with CustomObjectScope({"dice_coef": dice_coef, "dice_loss": dice_loss}):
        model = tf.keras.models.load_model(model_path)

        SCORE = []
        DICE_SCORE = []

        print(len(x_test))
        print(len(y_test))

        for x, y in tqdm(zip(x_test, y_test), total=len(y_test)):
            name = x.split("/")[-1]

            """Reading the image"""
            x = read_image(x)
            x = np.expand_dims(x, axis=0)

            """Reading mask"""
            y = read_mask(y)
            y = np.argmax(y, axis=-1)
            y = y.astype(np.int32)

            """Prediction"""
            y_pred = model.predict(x, verbose=0)[0]
            y_pred = np.argmax(y_pred, axis=-1)
            y_pred = y_pred.astype(np.int32)

            y = y.flatten()
            y_pred = y_pred.flatten()

            """Calculating metrics"""
            f1_value = f1_score(y, y_pred, average="micro")
            jac_value = jaccard_score(
                y, y_pred, average="micro")
            recall_value = recall_score(
                y, y_pred, average="micro", zero_division=0)
            precision_value = precision_score(
                y, y_pred, average="micro", zero_division=0)

            SCORE.append([name, f1_value, jac_value,
                          recall_value, precision_value])

            """Calculating dice score"""
            dice_score_per_class_result = dice_score_per_class(
                y, y_pred, 12)
            DICE_SCORE.append(dice_score_per_class_result)

        """ Metrics values """
        score = [s[1:]for s in SCORE]
        score = np.mean(score, axis=0)
        print(f"F1: {score[0]:0.5f}")
        print(f"Jaccard: {score[1]:0.5f}")
        print(f"Recall: {score[2]:0.5f}")
        print(f"Precision: {score[3]:0.5f}")

        """Save average score"""
        with open(os.path.join("files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_average-metrics_normal.csv"), "w") as f:
            f.write(f"F1, Jaccard, Recall, Precision")
            f.write(f"{score[0]}, {score[1]}, {score[2]}, {score[3]}\n")

        df = pd.DataFrame(
            SCORE, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
        df.to_csv(os.path.join("files", f"{VIEW}", "normal_training",
                               f"{VIEW}_dice-loss_metrics_normal.csv"))

        dice_score_df = pd.DataFrame(DICE_SCORE, columns=["background",
                                                          "left_ventricle",
                                                          "right_ventricle",
                                                          "left_atrium",
                                                          "right_atrium",
                                                          "myocardium",
                                                          "descending_aorta",
                                                          "pulmonary_trunk",
                                                          "ascending_aorta",
                                                          "vena_cava",
                                                          "auricle",
                                                          "coronary_artery"])
        dice_score_df.to_csv(os.path.join(
            "files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_dice-score-metric_normal.csv"))


def test_model_with_dice_in_training_with_frozen_graph(x_test, y_test, frozen_graph_path):
    with CustomObjectScope({"dice_coef": dice_coef, "dice_loss": dice_loss}):
        with tfc.gfile.GFile(frozen_graph_path, "rb") as f:
            graph_def = tfc.GraphDef()
            graph_def.ParseFromString(f.read())

        sess.graph.as_default()
        tfc.import_graph_def(graph_def)

        input_tensor = sess.graph.get_tensor_by_name("x:0")
        output_tensor = sess.graph.get_tensor_by_name("Identity:0")

        SCORE = []
        DICE_SCORE = []

        print(len(x_test))
        print(len(y_test))

        for x, y in tqdm(zip(x_test, y_test), total=len(y_test)):

            name = x.split("/")[-1]

            """Reading the image"""
            x = read_image(x)
            x = np.expand_dims(x, axis=0)
            x = np.expand_dims(x, axis=-1)

            """Reading mask"""
            y = read_mask(y)
            y = np.argmax(y, axis=-1)
            y = y.astype(np.int32)

            """Prediction"""
            y_pred = sess.run(output_tensor, {'x:0': x})[0]
            y_pred = np.argmax(y_pred, axis=-1)
            y_pred = y_pred.astype(np.int32)

            y = y.flatten()
            y_pred = y_pred.flatten()

            """Calculating metrics"""
            f1_value = f1_score(y, y_pred, average="micro")
            jac_value = jaccard_score(
                y, y_pred, average="micro")
            recall_value = recall_score(
                y, y_pred, average="micro", zero_division=0)
            precision_value = precision_score(
                y, y_pred, average="micro", zero_division=0)

            SCORE.append([name, f1_value, jac_value,
                          recall_value, precision_value])

            """Calculating dice score"""
            dice_score_per_class_result = dice_score_per_class(
                y, y_pred, 12)
            DICE_SCORE.append(dice_score_per_class_result)

        """ Metrics values """
        score = [s[1:]for s in SCORE]
        score = np.mean(score, axis=0)
        print(f"F1: {score[0]:0.5f}")
        print(f"Jaccard: {score[1]:0.5f}")
        print(f"Recall: {score[2]:0.5f}")
        print(f"Precision: {score[3]:0.5f}")

        """Save average score"""
        with open(os.path.join("files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_average-metrics_normal.csv"), "w") as f:
            f.write(f"F1, Jaccard, Recall, Precision")
            f.write(f"{score[0]}, {score[1]}, {score[2]}, {score[3]}\n")

        df = pd.DataFrame(
            SCORE, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
        df.to_csv(os.path.join("files", f"{VIEW}", "normal_training",
                               f"{VIEW}_dice-loss_metrics_normal.csv"))

        dice_score_df = pd.DataFrame(DICE_SCORE, columns=["background",
                                                          "left_ventricle",
                                                          "right_ventricle",
                                                          "left_atrium",
                                                          "right_atrium",
                                                          "myocardium",
                                                          "descending_aorta",
                                                          "pulmonary_trunk",
                                                          "ascending_aorta",
                                                          "vena_cava",
                                                          "auricle",
                                                          "coronary_artery"])
        dice_score_df.to_csv(os.path.join(
            "files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_dice-score-metric_normal.csv"))


def test_model_without_dice_in_training(x_test, y_test, model_path):
    model = tf.keras.models.load_model(model_path)

    SCORE = []
    DICE_SCORE = []

    for x, y in tqdm(zip(x_test, y_test), total=len(y_test)):
        name = x.split("/")[-1]

        """Reading the image"""
        x = read_image(x)
        x = np.expand_dims(x, axis=0)

        """Reading mask"""
        y = read_mask(y)
        y = np.argmax(y, axis=-1)
        y = y.astype(np.int32)

        """Prediction"""
        y_pred = model.predict(x, verbose=0)[0]
        y_pred = np.argmax(y_pred, axis=-1)
        y_pred = y_pred.astype(np.int32)

        y = y.flatten()
        y_pred = y_pred.flatten()

        """Calculating metrics"""
        f1_value = f1_score(y, y_pred, average="micro")
        jac_value = jaccard_score(
            y, y_pred, average="micro")
        recall_value = recall_score(
            y, y_pred, average="micro", zero_division=0)
        precision_value = precision_score(
            y, y_pred, average="micro", zero_division=0)

        SCORE.append([name, f1_value, jac_value,
                      recall_value, precision_value])

        """Calculating dice score"""
        dice_score_per_class_result = dice_score_per_class(
            y, y_pred, 12)
        DICE_SCORE.append(dice_score_per_class_result)

    """ Metrics values """
    score = [s[1:]for s in SCORE]
    score = np.mean(score, axis=0)
    print(f"F1: {score[0]:0.5f}")
    print(f"Jaccard: {score[1]:0.5f}")
    print(f"Recall: {score[2]:0.5f}")
    print(f"Precision: {score[3]:0.5f}")

    """Save average score"""
    with open(os.path.join("files", f"{VIEW}", "normal_training", f"{VIEW}_average-metrics_normal.csv"), "w") as f:
        f.write(f"F1, Jaccard, Recall, Precision")

        f.write(f"{score[0]}, {score[1]}, {score[2]}, {score[3]}\n")

    df = pd.DataFrame(
        SCORE, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
    df.to_csv(os.path.join("files", f"{VIEW}", "normal_training",
                           f"{VIEW}_metrics_normal.csv"))

    dice_score_df = pd.DataFrame(DICE_SCORE, columns=["background",
                                                      "left_ventricle",
                                                      "right_ventricle",
                                                      "left_atrium",
                                                      "right_atrium",
                                                      "myocardium",
                                                      "descending_aorta",
                                                      "pulmonary_trunk",
                                                      "ascending_aorta",
                                                      "vena_cava",
                                                      "auricle",
                                                      "coronary_artery"])
    dice_score_df.to_csv(os.path.join(
        "files", f"{VIEW}", "normal_training", f"{VIEW}_dice-score-metric_normal.csv"))


if __name__ == "__main__":
    """Params"""
    VIEW = "coronal"

    sess = tfc.InteractiveSession()
    frozen_graph = "E:\\ISEF\\VHSCDD\\frozen_graph\\coronal_dice-loss_frozen_graph.pb"

    """Testing"""
    (x_train, y_train), (x_val, y_val), (x_test,
                                         y_test) = load_dataset(".\\files", view=VIEW)

    # model_path = "C:\\Users\\Acer\\OneDrive\\Documents\\Model Data\\saggital_dice-loss_model_normal.h5"
    # test_model_with_dice_in_training(x_test, y_test, model_path)

    test_model_with_dice_in_training_with_frozen_graph(
        x_test, y_test, frozen_graph)
