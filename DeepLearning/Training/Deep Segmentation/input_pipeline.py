import os
import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tfc
import nibabel as nib
import time
from metrics import dice_coef, dice_loss
from keras import backend as K
from glob import glob
import cv2
import segmentation_models as sm


focal_loss = sm.losses.CategoricalFocalLoss(gamma=4)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=6040)]
    )


def normalize_image_intensity_range(img):
    HOUNSFIELD_MAX = 4000
    HOUNSFIELD_MIN = 0
    HOUNSFIELD_RANGE = HOUNSFIELD_MAX - HOUNSFIELD_MIN
    img[img < HOUNSFIELD_MIN] = HOUNSFIELD_MIN
    img[img > HOUNSFIELD_MAX] = HOUNSFIELD_MAX

    return (img - HOUNSFIELD_MIN) / HOUNSFIELD_RANGE


def save_image_for_inference(img_path, view="axial"):
    array = nib.load(
        sorted(glob(os.path.join(img_path, "*.nii.gz")))[0]).get_fdata()
    array = normalize_image_intensity_range(array)

    if view == "axial":
        for i in range(array.shape[-1]):
            img_slice = array[:, :, i]
            img_name = f"heart{0}-slice{str(i).zfill(3)}_axial"
            # img = cv2.resize(img_slice, (IMG_W, IMG_H))
            img = np.uint8(img_slice * 255)

            path = os.path.join("inference", f"{img_name}.png")

            print(f"Image name: {img_name}")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")

    elif view == "saggital":
        for i in range(array.shape[1]):
            img_slice = array[:, i, :]
            img_name = f"heart{0}-slice{str(i).zfill(3)}_saggital"
            # img = cv2.resize(img_slice, (IMG_W, IMG_Z))
            img = np.uint8(img_slice * 255)

            path = os.path.join("inference", f"{img_name}.png")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")

    elif view == "coronal":
        for i in range(array.shape[0]):
            img_slice = array[i, :, :]
            img_name = f"heart{0}-slice{str(i).zfill(3)}_coronal"
            # img = cv2.resize(img_slice, (IMG_H, IMG_Z))
            img = np.uint8(img_slice * 255)

            path = os.path.join("inference", f"{img_name}.png")

            res = cv2.imwrite(path, img)
            if not res:
                print(f"Error, unable to save image with name: {img_name}")


def load_dataset_for_inference(view="axial"):
    images = sorted(
        glob(os.path.join("inference", f"*_{view}.png")))
    return images


def read_image(x):
    x = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
    # x = cv2.resize(x, (512, 600))
    x = x / 255.0
    x = x.astype(np.float32)
    return x


def preprocess(x):
    def f(x):
        x = x.decode()

        x = read_image(x)
        return x

    image = tf.numpy_function(f, [x], tf.float32)
    image.set_shape([600, 600])

    return image


def tf_dataset(x, batch=2):
    dataset = tf.data.Dataset.from_tensor_slices((x))
    dataset = dataset.map(preprocess)
    dataset = dataset.batch(batch)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    return dataset


def old_pipeline(model_path, img_path: str, save_path: str, view: str = None, batch_size=2):

    model = tf.keras.models.load_model(model_path, custom_objects={
                                       "focal_loss": focal_loss, "dice_coef": dice_coef})

    save_image_for_inference(img_path, view=view)

    if view != None:
        dataset = load_dataset_for_inference(view=view)
        dataset = tf_dataset(dataset)
        start_time = time.time()
        predictions = []

        for x in dataset:
            pred = model.predict(x, verbose=0).argmax(axis=-1)
            predictions.extend(pred)

        end_time = time.time()

        print(f"Total time: {end_time - start_time}")

        if view == "axial":
            predictions = np.stack(predictions, axis=-1).astype(np.int32)
        elif view == "saggital":
            predictions = np.stack(predictions, axis=1).astype(np.int32)
        else:
            predictions = np.stack(predictions, axis=0).astype(np.int32)

        print(predictions.shape)

        nifti_image = nib.nifti1.Nifti1Image(
            predictions, affine=np.eye(4), dtype=np.int32)
        nib.save(nifti_image, save_path)
        # np.save(f"{view}_predict.npy", predictions)


def pipeline_for_1view(frozen_path, img_path, save_path, view="axial", batch_size=2):
    array = nib.load(img_path).get_fdata()
    array = normalize_image_intensity_range(array)
    array = array.astype(np.float32)
    predictions = []

    sess = tfc.InteractiveSession()
    with tfc.gfile.GFile(frozen_path, "rb") as f:
        graph_def = tfc.GraphDef()
        graph_def.ParseFromString(f.read())

    sess.graph.as_default()
    tfc.import_graph_def(graph_def)
    input_tensor = sess.graph.get_tensor_by_name("x:0")
    output_tensor = sess.graph.get_tensor_by_name(
        "Identity:0")

    if view == "axial":
        dataset = [np.expand_dims(array[:, :, i], -1)
                   for i in range(array.shape[-1])]
    elif view == "saggital":
        dataset = [np.expand_dims(array[:, i, :], -1)
                   for i in range(array.shape[1])]
    elif view == "coronal":
        dataset = [np.expand_dims(array[i, :, :], -1)
                   for i in range(array.shape[0])]
    print("start")
    start_time = time.time()
    for x in dataset:
        x = np.expand_dims(x, axis=0)
        subpredictions = sess.run(
            output_tensor, {'x:0': x})[0]
        subpredictions = np.argmax(subpredictions, axis=-1).astype(np.uint8)
        predictions.append(subpredictions)

    if view == "axial":
        predictions = np.stack(predictions, axis=-1)
    elif view == "saggital":
        predictions = np.stack(predictions, axis=1)
    elif view == "coronal":
        predictions = np.stack(predictions, axis=0)

    np.save(f"./output/{view}_predict.npy", predictions)
    print("end")
    end_time = time.time()
    print(f"Time: {end_time - start_time}")


if __name__ == "__main__":
    # model_path = "C:\\Users\\Acer\\OneDrive\\Documents\\Model Data\\axial_dice-loss_model_normal.h5"
    model_path = "./Optimized Model and Graph/axial_focal_5.h5"
    save_path = "./output/axial_predict_5.nii"
    img_path = "./VHSCDD images/VHSCDD_020_image/"
    # frozen_path = "E:\\ISEF\\VHSCDD\\frozen_graph\\optimized\\axial_dice-loss_optimized_frozen_graph.pb"
    # frozen_path = "./Optimized Model and Graph/coronal_frozen_graph.pb"
    old_pipeline(model_path, img_path, save_path, view="axial")
    # pipeline_for_1view(frozen_path, img_path, save_path, view="coronal")
