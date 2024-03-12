import os
import numpy as np
import pandas as pd
import cv2
from glob import glob
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, CSVLogger
from unet_attention import Attention_Unet
import nibabel as nib
import matplotlib.pyplot as plt
import re
import skimage.transform as skTrans
from metrics import dice_loss, dice_coef


# physical_devices = tf.config.list_physical_devices('GPU')

# # Enable memory growth for each GPU
# for device in physical_devices:
#     tf.config.experimental.set_memory_growth(device, True)

"""Global parameters"""
global IMG_H
global IMG_W
global IMG_Z
global NUM_CLASSES
global CLASSES
global HOUNSFIELD_MIN
global HOUNSFIELD_MAX
global HOUNSFIELD_RANGE
global MASK_NORMALIZE
global SLICE_DECIMATE_IDENTIFIER
global BATCH_SIZE
global VIEW


def extract_label_number(path):
    # Extract the label number from the file name using regular expression
    match = re.search(r'ct_\d+_label_(\d+)\.nii', path)
    if match:
        return int(match.group(1))
    else:
        return -1  # Return -1 if no label number is found


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def convert_multiclass_to_binary_mask(a: np.array):
    uniques = sorted(np.unique(a))

    for num in uniques:
        if num == 0:
            continue
        elif num == 1:
            continue
        elif num > 1:
            a[a == num] = 1


def save_image(img_path: str, nii_index: int, view: str = "axial"):
    array = nib.load(
        sorted(glob(os.path.join(img_path, "*.nii.gz")))[0]).get_fdata()
    array = normalize_image_intensity_range(array)

    if view == "axial":
        for i in range(array.shape[-1]):
            img_slice = array[:, :, i]
            img_name = f"heart{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_axial"
            img = cv2.resize(img_slice, (IMG_W, IMG_H))
            img = np.uint8(img * 255)

            path = os.path.join("files", "images", f"{img_name}.png")

            print(f"Image name: {img_name}")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")

    elif view == "saggital":
        for i in range(array.shape[1]):
            img_slice = array[:, i, :]
            img_name = f"heart{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_saggital"
            # img = cv2.resize(img_slice, (IMG_W, IMG_Z))
            img = np.uint8(img_slice * 255)

            path = os.path.join("files", "images", f"{img_name}.png")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")

    elif view == "coronal":
        for i in range(array.shape[0]):
            img_slice = array[i, :, :]
            img_name = f"heart{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_coronal"
            # img = cv2.resize(img_slice, (IMG_H, IMG_Z))
            img = np.uint8(img_slice * 255)

            path = os.path.join("files", "images", f"{img_name}.png")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")


def save_mask(mask_path: str, nii_index: int, view="axial"):
    separate_mask_path = sorted(
        glob(os.path.join(mask_path, "output", "*.nii")), key=extract_label_number)

    """Get labels from .nii files"""
    label_1 = np.uint(nib.load(separate_mask_path[1]).get_fdata())
    label_2 = np.uint(nib.load(separate_mask_path[2]).get_fdata())
    label_3 = np.uint(nib.load(separate_mask_path[3]).get_fdata())
    label_4 = np.uint(nib.load(separate_mask_path[4]).get_fdata())
    label_5 = np.uint(nib.load(separate_mask_path[5]).get_fdata())
    label_6 = np.uint(nib.load(separate_mask_path[6]).get_fdata())
    label_7 = np.uint(nib.load(separate_mask_path[7]).get_fdata())
    label_8 = np.uint(nib.load(separate_mask_path[8]).get_fdata())
    label_9 = np.uint(nib.load(separate_mask_path[9]).get_fdata())
    label_10 = np.uint(nib.load(separate_mask_path[10]).get_fdata())
    label_11 = np.uint(nib.load(separate_mask_path[11]).get_fdata())

    label_0 = np.ones((IMG_W, IMG_H, IMG_Z))

    """Convert to binary (0, 1)"""
    convert_multiclass_to_binary_mask(label_1)
    convert_multiclass_to_binary_mask(label_2)
    convert_multiclass_to_binary_mask(label_3)
    convert_multiclass_to_binary_mask(label_4)
    convert_multiclass_to_binary_mask(label_5)
    convert_multiclass_to_binary_mask(label_6)
    convert_multiclass_to_binary_mask(label_7)
    convert_multiclass_to_binary_mask(label_8)
    convert_multiclass_to_binary_mask(label_9)
    convert_multiclass_to_binary_mask(label_10)
    convert_multiclass_to_binary_mask(label_11)

    """Create stack & encoded array"""
    label_list = [label_0, label_1, label_2, label_3, label_4,
                  label_5, label_6, label_7, label_8, label_9, label_10, label_11]
    for i in range(1, len(label_list)):
        label_0[label_list[i] == 1] = 0
    output = np.stack(label_list, axis=-1)

    if view == "axial":
        for i in range(output.shape[2]):

            mask = output[:, :, i, :]
            # mask = np.uint(cv2.resize(mask, (IMG_W, IMG_H, 12)))

            mask_name = f"heartmaskencode{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_axial"
            path = os.path.join("files", "masks", f"{mask_name}.npy")
            np.save(path, mask)

            print(f"Mask name: {mask_name}")

    elif view == "saggital":
        for i in range(output.shape[1]):
            mask = output[:, i, :, :]
            # mask = np.uint(cv2.resize(mask, (IMG_W, IMG_H, 12)))

            mask_name = f"heartmaskencode{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_saggital"
            path = os.path.join("files", "masks", f"{mask_name}.npy")
            np.save(path, mask)

    elif view == "coronal":
        for i in range(output.shape[0]):

            mask = output[i, :, :, :]
            # mask = np.uint(cv2.resize(mask, (IMG_W, IMG_H, 12)))

            mask_name = f"heartmaskencode{nii_index}-slice{str(i).zfill(SLICE_DECIMATE_IDENTIFIER)}_coronal"
            path = os.path.join("files", "masks", f"{mask_name}.npy")
            np.save(path, mask)


def normalize_image_intensity_range(img):
    img[img < HOUNSFIELD_MIN] = HOUNSFIELD_MIN
    img[img > HOUNSFIELD_MAX] = HOUNSFIELD_MAX

    return (img - HOUNSFIELD_MIN) / HOUNSFIELD_RANGE


def volumetric_to_slice(image_path, mask_path, view="axial", custom_counter: int = None):
    image_sub = sorted(glob(os.path.join(image_path, "*")))
    mask_sub = sorted(glob(os.path.join(mask_path, "*")))

    custom_counter_flag = custom_counter != None
    if view == "axial":
        for nii_index in range(len(image_sub)):
            image_path = image_sub[nii_index]
            mask_path = mask_sub[nii_index]

            if not custom_counter_flag:
                save_mask(mask_path, nii_index, view=view)
                save_image(image_path, nii_index, view=view)
            else:
                save_mask(mask_path, custom_counter, view=view)
                save_image(image_path, custom_counter, view=view)
                custom_counter += 1

    elif view == "saggital":
        for nii_index in range(len(image_sub)):
            image_path = image_sub[nii_index]
            mask_path = mask_sub[nii_index]

            if not custom_counter_flag:
                save_mask(mask_path, nii_index, view=view)
                save_image(image_path, nii_index, view=view)

            else:
                save_mask(mask_path, custom_counter, view=view)
                save_image(image_path, custom_counter, view=view)
                custom_counter += 1

    if view == "coronal":
        for nii_index in range(len(image_sub)):
            image_path = image_sub[nii_index]
            mask_path = mask_sub[nii_index]

            if not custom_counter_flag:
                save_mask(mask_path, nii_index, view=view)
                save_image(image_path, nii_index, view=view)
            else:
                save_mask(mask_path, custom_counter, view=view)
                save_image(image_path, custom_counter, view=view)
                custom_counter += 1


def load_dataset(path, split=0.2, view="axial"):
    images = sorted(
        glob(os.path.join(path, "images", f"*_{view}.png")))
    masks = sorted(
        glob(os.path.join(path, "masks", f"*_{view}.npy")))

    print(f"Image: {len(images)} || Mask: {len(masks)}")

    split_size = int(split * len(images))

    x_train, x_val = train_test_split(
        images, test_size=split_size, random_state=42)

    y_train, y_val = train_test_split(
        masks, test_size=split_size, random_state=42)

    x_train, x_test = train_test_split(
        x_train, test_size=split_size, random_state=42)

    y_train, y_test = train_test_split(
        y_train, test_size=split_size, random_state=42)

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)


def specific_case_load_dataset(path, split=0.2, view="axial"):
    images = sorted(
        glob(os.path.join(path, "images", f"*_{view}.png")))

    masks = sorted(
        glob(os.path.join(path, "masks", f"*_{view}.npy")))

    print(f"Image: {len(images)} || Mask: {len(masks)}")

    split_size = int(len(images) / 512 * split)

    index_chosen = set()

    x_train = []
    y_train = []
    x_test = []
    y_test = []
    x_val = []
    y_val = []

    R = np.random.RandomState(seed=42)

    "Generate Test & Validation"
    counter = 0
    while counter < split_size:
        i = R.randint(0, 34)

        if i not in index_chosen:
            counter += 1
            index_chosen.add(i)

            x_test_extend = glob(os.path.join(
                path, "images", f"heart{i}-*_{view}.png"))
            x_test += x_test_extend

            y_test_extend = glob(os.path.join(path, "masks",
                                              f"heartmaskencode{i}-*_{view}.npy"))
            y_test += y_test_extend

    counter = 0
    while counter < split_size:
        i = R.randint(0, 34)

        if i not in index_chosen:
            counter += 1
            index_chosen.add(i)

            x_val_extend = glob(os.path.join(
                path, "images", f"heart{i}-*_{view}.png"))
            x_val += x_val_extend

            y_val_extend = glob(os.path.join(path, "masks",
                                             f"heartmaskencode{i}-*_{view}.npy"))
            y_val += y_val_extend

    counter = 0
    while counter < 34 - 2*split_size:
        i = R.randint(0, 34)

        if i not in index_chosen:
            counter += 1
            index_chosen.add(i)

            x_train_extend = glob(os.path.join(
                path, "images", f"heart{i}-*_{view}.png"))
            x_train += x_train_extend

            y_train_extend = glob(os.path.join(path, "masks",
                                               f"heartmaskencode{i}-*_{view}.npy"))
            y_train += y_train_extend

    return (sorted(x_train), sorted(y_train)), (sorted(x_val), sorted(y_val)), (sorted(x_test), sorted(y_test))


def read_image(x):
    x = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
    # x = cv2.resize(x, (512, 600))
    x = x / 255.0
    x = x.astype(np.float32)
    return x


def read_mask(x):
    x = np.load(x)
    # x = skTrans.resize(x, (400, 400, 12), preserve_range=True)
    # x = x.astype(np.uint8)
    x = x.astype(np.float32)

    return x


def preprocess(x, y):
    def f(x, y):
        x = x.decode()
        y = y.decode()

        x = read_image(x)
        y = read_mask(y)

        return x, y

    image, mask = tf.numpy_function(f, [x, y], [tf.float32, tf.float32])
    image.set_shape([600, 512])
    mask.set_shape([600, 512, 12])

    return image, mask


def tf_dataset(x, y, batch=1):
    dataset = tf.data.Dataset.from_tensor_slices((x, y))
    dataset = dataset.shuffle(buffer_size=5000)
    dataset = dataset.map(preprocess)
    dataset = dataset.batch(batch)
    dataset = dataset.prefetch(1)
    return dataset


if __name__ == "__main__":
    """Seeding"""
    np.random.seed(42)
    tf.random.set_seed(42)

    """Create directory to save files"""
    create_dir("files")

    """Path"""
    image_path = "E:\ISEF\VHSCDD\VHSCDD images"
    mask_path = "E:\ISEF\VHSCDD\VHSCDD labels"

    """Hyperparameters"""
    IMG_W = 600
    IMG_H = 600
    IMG_Z = 512
    HOUNSFIELD_MAX = 4000
    HOUNSFIELD_MIN = 0
    HOUNSFIELD_RANGE = HOUNSFIELD_MAX - HOUNSFIELD_MIN
    NUM_CLASSES = 12
    CLASSES = [
        "background",
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
        "coronary_artery"
    ]
    SLICE_DECIMATE_IDENTIFIER = 3
    BATCH_SIZE = 4
    VIEW = "coronal"

    input_shape = (600, 512, 1)
    lr = 1e-4
    num_epochs = 15

    # model_path = os.path.join(
    #     "files", f"{VIEW}", "normal_training", f"{VIEW}_model_normal.h5")
    # csv_path = os.path.join(
    #     "files", f"{VIEW}", "normal_training", f"{VIEW}_data_normal.csv")

    model_path = os.path.join(
        "files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_model_normal.h5")
    csv_path = os.path.join(
        "files", f"{VIEW}", "normal_training", f"{VIEW}_dice-loss_data_normal.csv")

    """Convert volumetric dataset to single slices"""
    # first time failed
    # volumetric_to_slice(image_path, mask_path, view=VIEW)

    # second time
    # volumetric_to_slice(image_path_separated,
    #                     mask_path_separated, view="axial", custom_counter=31)

    """Load dataset"""
    (x_train, y_train), (x_val, y_val), (x_test,
                                         y_test) = specific_case_load_dataset("files", split=0.2, view=VIEW)

    """Load tf dataset"""
    train_dataset = tf_dataset(x_train, y_train, batch=BATCH_SIZE)
    valid_dataset = tf_dataset(x_val, y_val, batch=BATCH_SIZE)
    test_dataset = tf_dataset(x_test, y_test, batch=BATCH_SIZE)

    """Model"""
    model = Attention_Unet(input_shape, NUM_CLASSES)
    # model.compile(loss="categorical_crossentropy",
    #               optimizer=tf.keras.optimizers.Adam(lr), metrics=["accuracy"])

    model.compile(loss=dice_loss, optimizer=tf.keras.optimizers.Adam(
        lr), metrics=[dice_coef, "accuracy"])

    """Training"""
    callbacks = [
        ModelCheckpoint(model_path, verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.1,
                          patience=5, min_lr=1e-7, verbose=1),
        CSVLogger(csv_path, append=True),
        EarlyStopping(monitor="val_loss", patience=20,
                      restore_best_weights=False)
    ]

    model.fit(train_dataset, validation_data=valid_dataset,
              epochs=num_epochs, callbacks=callbacks)
