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

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=10000)]
    )

logical_gpus = tf.config.list_logical_devices('GPU')
print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")


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
    dataset = dataset.cache()
    dataset = dataset.map(preprocess)
    dataset = dataset.batch(batch)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    return dataset


def old_pipeline(model_path, img_path: str, save_path: str, view: str = None, batch_size=2):

    model = tf.keras.models.load_model(model_path, custom_objects={
                                       "dice_loss": dice_loss, "dice_coef": dice_coef})

    array = nib.load(img_path).get_fdata()
    array = normalize_image_intensity_range(array)
    array = array.astype(np.float16)

    # save_image_for_inference(img_path, view=view)

    if view != None:
        if view == "axial":
            dataset = [array[:, :, i] for i in range(array.shape[-1])]
            predictions = []
            # dataset = load_dataset_for_inference(view="axial")
            # dataset = tf_dataset(dataset)
            start_time = time.time()

            for i in range(0, len(dataset)):
                subset = [dataset[j]
                          for j in range(i, i + 6) if j < len(dataset)]

                subset = tf.data.Dataset.from_tensor_slices(subset)
                subset = subset.batch(2)

                subpredictions = model.predict(subset)
                predictions.extend(subpredictions)

            # dataset = tf.data.Dataset.from_tensor_slices(dataset)
            # dataset = dataset.batch(1)
            # dataset = dataset.prefetch(1)

            # for batch in dataset:
            #     subpredictions = model.predict(np.expand_dims(batch, axis=0))
            #     K.clear_session()

            # predictions = model.predict(dataset)
            # predictions = np.argmax(predictions, axis=-1)
            end_time = time.time()

            print(f"Total time: {end_time - start_time}")

            # predictions = np.array(predictions)
            # nifti_image = nib.nifti1.Nifti1Image(
            #     predictions, affine=affine_matrix)
            # nib.save(nifti_image, save_path)

        elif view == "saggital":
            dataset = [array[:, i, :] for i in range(array.shape[1])]
            dataset = tf.data.Dataset.from_tensor_slices(dataset)
            dataset = dataset.batch(batch_size)

            predictions = model.predict(dataset)
            predictions = np.argmax(predictions, axis=-1)

            nifti_image = nib.nifti1.Nifti1Image(predictions)
            nib.save(nifti_image, save_path)

        elif view == "coronal":
            dataset = [array[i, :, :] for i in range(array.shape[0])]
            dataset = tf.data.Dataset.from_tensor_slices(dataset)
            dataset = dataset.batch(batch_size)

            predictions = model.predict(dataset)
            predictions = np.argmax(predictions, axis=-1)

            nifti_image = nib.nifti1.Nifti1Image(predictions)
            nib.save(nifti_image, save_path)

    else:
        axial_dataset = [array[:, :, i] for i in range(array.shape[-1])]
        axial_dataset = tf.data.Dataset.from_tensor_slices(axial_dataset)
        axial_dataset = axial_dataset.batch(batch_size)

        axial_predictions = model.predict(axial_dataset)
        axial_predictions = np.argmax(axial_predictions, axis=-1)

        saggital_dataset = [array[:, i, :] for i in range(array.shape[1])]
        saggital_dataset = tf.data.Dataset.from_tensor_slices(
            saggital_dataset)
        saggital_dataset = saggital_dataset.batch(batch_size)

        saggital_predictions = model.predict(saggital_dataset)
        saggital_predictions = np.argmax(saggital_predictions, axis=-1)

        coronal_dataset = [array[i, :, :] for i in range(array.shape[0])]
        coronal_dataset = tf.data.Dataset.from_tensor_slices(
            coronal_dataset)
        coronal_dataset = coronal_dataset.batch(batch_size)

        coronal_predictions = model.predict(coronal_dataset)
        coronal_predictions = np.argmax(coronal_predictions, axis=-1)

        intersection = np.where((axial_predictions == saggital_predictions) & (
            saggital_predictions == coronal_predictions), axial_predictions, 0)


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


def triple_view_intersection():
    axial_dice_score = {
        0: 0.9967,
        1: 0.7099,
        2: 0.8344,
        3: 0.7705,
        4: 0.8097,
        5: 0.7976,
        6: 0.8566,
        7: 0.7515,
        8: 0.6153,
        9: 0.5389,
        10: 0.8317,
        11: 0.6057
    }

    # saggital_dice_score = {
    #     0: -1, 1: -1, 2: -1, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: -1, 9: 7, 10: -1, 11: 11
    # }

    saggital_dice_score = {
        0: 0.9956,
        1: 0.7777,
        2: 0.7950,
        3: 0.8008,
        4: 0.9298,
        5: 0.9220,
        6: 0.9429,
        7: 0.8701,
        8: 0.8039,
        9: 0.8414,
        10: 0.8424,
        11: 0.6679
    }

    # coronal_dice_score = {
    #     0: -1, 1: 1, 2: 2, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: 8, 9: -1, 10: 10, 11: -1
    # }
    coronal_dice_score = {
        0: 0.9921,
        1: 0.9201,
        2: 0.8975,
        3: 0.7834,
        4: 0.8924,
        5: 0.9001,
        6: 0.8395,
        7: 0.7513,
        8: 0.8934,
        9: 0.7765,
        10: 0.8574,
        11: 0.6390
    }

    axial = np.load("./output/axial_predict.npy")
    saggital = np.load("./output/saggital_predict.npy")
    coronal = np.load("./output/coronal_predict.npy")

    axial_v = np.vectorize(axial_dice_score.__getitem__)(axial)
    saggital_v = np.vectorize(saggital_dice_score.__getitem__)(saggital)
    coronal_v = np.vectorize(coronal_dice_score.__getitem__)(coronal)

    # max_values = np.maximum.reduce([axial_v, saggital_v, coronal_v])
    # print(max_values.shape)

    # how about counting most common and not necessarily the same for 3 models ?

    start_time = time.time()
    # intersection = np.where(max_values == axial_v, axial,
    #                         np.where(max_values == saggital_v, saggital, coronal))
    intersection = np.empty_like(axial)
    for i in range(axial.shape[0]):
        for j in range(axial.shape[1]):
            for k in range(axial.shape[2]):
                counter = np.zeros(11)
                counter[axial[i][j][k]] += 1
                counter[saggital[i][j][k]] += 1
                counter[coronal[i][j][k]] += 1

                choice = np.argwhere(
                    counter == max(counter)).squeeze(axis=-1)

                if len(choice) == 1:
                    intersection[i][j][k] = choice[0]
                else:
                    max_index = np.argmax(
                        [axial_v[i, j, k], saggital_v[i, j, k], coronal_v[i, j, k]])
                    if max_index == 0:
                        intersection[i][j][k] = axial[i][j][k]
                    elif max_index == 1:
                        intersection[i][j][k] = saggital[i][j][k]
                    else:
                        intersection[i][j][k] = coronal[i][j][k]

    print(intersection.shape)
    end_time = time.time()

    print(f"Time: {end_time - start_time}")

    new_image = nib.Nifti1Image(intersection, affine=np.eye(4))
    nib.save(new_image, "./output/intersection.nii")

    np.save("./output/intersection.npy", intersection)


if __name__ == "__main__":
    # model_path = "C:\\Users\\Acer\\OneDrive\\Documents\\Model Data\\axial_dice-loss_model_normal.h5"
    # old_pipeline(model_path, img_path, save_path, view="axial")
    model_path = "./Optimized Model and Graph/axial.h5"
    save_path = ".\\testing.nii.gz"
    img_path = "E:\\ISEF\\VHSCDD\\VHSCDD images\\VHSCDD_020_image\\ct_020_image.nii.gz"
    # frozen_path = "E:\\ISEF\\VHSCDD\\frozen_graph\\optimized\\axial_dice-loss_optimized_frozen_graph.pb"
    frozen_path = "./Optimized Model and Graph/coronal_frozen_graph.pb"
    # pipeline_for_1view(frozen_path, img_path, save_path, view="coronal")

    triple_view_intersection()
