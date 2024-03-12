from Unet.unet import build_unet
from train import load_dataset
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
import os
from k_fold_training import load_dataset_kfold, read_image, read_mask
from train import load_dataset, tf_dataset
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def get_csv_indices(kfold=0):
    file = sorted(
        glob(os.path.join("files", "saggital", "index_info")))[kfold]
    train = []
    test = []
    with open(file, 'r') as f:
        content = f.readlines()

        for i in range(len(content)):
            if f[i] == "train":
                j = i + 1
                while f[j] != "test" and j < len(content):
                    index = int(f[j])
                    train.append(index)
                    j += 1
                i = j - 1

            elif f[i] == "test":
                j = i + 1
                while f[j] != "train" and j < len(content):
                    index = int(f[j])
                    test.append(index)
                    j += 1
                i = j - 1

    train = np.array(train)
    test = np.array(test)

    return (train, test)


if __name__ == "__main__":
    x, y = load_dataset_kfold(os.path.join("files"), view="saggital")

    with CustomObjectScope({"dice_coef": dice_coef, "dice_loss": dice_loss}):
        model = tf.keras.models.load_model(
            os.path.join("files", "saggital", "saggital_fold-0.h5"))

        kfold = 4
        for i in range(kfold):
            train_index, test_index = get_csv_indices(i)

            x_test = x[test_index].tolist()
            y_test = y[test_index].tolist()

            SCORE = []
            DICE_SCORE = []

            for x, y in tqdm(zip(x_test, y_test), total=len(y_test)):
                name = x.split("/")[-1]

                """Reading the image"""
                x = read_image(x)
                x = np.expand_dims(x, axis=0)

                """Reading mask"""
                y = read_mask(y)

                """Prediction"""
                y_pred = model.predict(x, verbose=0)[0]
                y_pred = np.argmax(y_pred, axis=-1)
                y_pred = y_pred.astype(np.int32)

                y = y.flatten()
                y_pred = y_pred.flatten()

                """Calculating metrics"""
                f1_value = f1_score(y, y_pred, average="macro")
                jac_value = jaccard_score(
                    y, y_pred, labels=[0, 1], average="macro")
                recall_value = recall_score(
                    y, y_pred, labels=[0, 1], average="macro", zero_division=0)
                precision_value = precision_score(
                    y, y_pred, labels=[0, 1], average="macro", zero_division=0)

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

            df = pd.DataFrame(
                SCORE, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
            df.to_csv(os.path.join("files", "saggital",
                      f"regular_metrics-{i}.csv"))

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
                "files", "saggital", f"dice_score_metrics-{i}.csv"))
