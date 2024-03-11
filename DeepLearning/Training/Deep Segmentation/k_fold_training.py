import numpy as np
from sklearn.model_selection import KFold
from train import read_image, read_mask, preprocess, tf_dataset
from metrics import dice_coef, dice_loss
from glob import glob
import os
import tensorflow as tf
from unet_attention import Attention_Unet
from Unet.unet import build_unet
from Resnet.resnet import build_resnet
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, CSVLogger
from sklearn.model_selection import train_test_split
from tqdm import tqdm

"""Global parameters"""
global NUM_CLASSES


def load_dataset_kfold(path, view="axial"):
    images = sorted(
        glob(os.path.join(path, "images", f"*_{view}.png")))
    masks = sorted(
        glob(os.path.join(path, "masks", f"*_{view}.npy")))

    print(f"Image: {len(images)} || Mask: {len(masks)}")

    return (np.array(images), np.array(masks))


if __name__ == "__main__":
    """Seeding"""
    np.random.seed(42)
    tf.random.set_seed(42)

    """Hyperparameters"""
    NUM_CLASSES = 12
    input_shape = (600, 512, 1)
    lr = 1e-4
    num_epochs = 15

    """Load KFold"""
    kfold = KFold(n_splits=4, shuffle=True)
    x, y = load_dataset_kfold(os.path.join("files"), view="saggital")

    """Training"""
    fold_count = 0
    for train, test in kfold.split(x, y):

        """Path"""
        model_path = os.path.join(
            "files", "saggital", f"saggital_fold-{fold_count}.h5")

        csv_path = os.path.join("files", "saggital",
                                f"saggital_data_kfold_{fold_count}.csv")

        x_train = x[train].tolist()
        y_train = y[train].tolist()

        x_val = x[test].tolist()
        y_val = y[test].tolist()

        # write indices for future saves
        with open(os.path.join("files", "saggital", "index_info", f"index_fold-{fold_count}.txt"), 'w') as f:
            f.write("Train\n")
            for index in train:
                f.write(f"{index}\n")
            f.write("Test\n")
            for index in test:
                f.write(f"{index}\n")

        # get testing dataset from validation dataset
        split_size = int(0.5 * len(x_val))
        x_val, x_test = train_test_split(
            x_val, test_size=split_size, random_state=42)
        y_val, y_test = train_test_split(
            y_val, test_size=split_size, random_state=42)

        train_dataset = tf_dataset(x_train, y_train, batch=4)
        valid_dataset = tf_dataset(x_val, y_val, batch=4)

        model = build_resnet(input_shape, NUM_CLASSES)
        model.compile(loss=dice_loss,
                      optimizer=tf.keras.optimizers.Adam(lr), metrics=[dice_coef, "accuracy"])

        callbacks = [
            ModelCheckpoint(model_path, verbose=1, save_best_only=True),
            ReduceLROnPlateau(monitor="val_loss", factor=0.1,
                              patience=5, min_lr=1e-7, verbose=1),
            CSVLogger(csv_path, append=True),
            EarlyStopping(monitor="val_loss", patience=20,
                          restore_best_weights=False)
        ]

        model.fit(train_dataset,
                  epochs=num_epochs, callbacks=callbacks)

        """Testing"""
