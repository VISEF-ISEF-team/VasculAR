import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import skimage.transform as skTrans
import cv2


def encoding_check(image: str = None, label: str = None, image_resize_shape=None, label_resize_shape=None):
    """
    image: Path to image in need of checking
    label: Path to label in need of checking 
    resize_shape to resize label and image 

    label should be the label of image
    """

    if image != None:
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

        if image_resize_shape != None:
            image = cv2.resize(image, image_resize_shape)
            image = image.astype(np.float32)
        cv2.imwrite("resize.png", image)

    if label != None:
        label = np.load(label)

        if label_resize_shape != None:
            label = skTrans.resize(
                label, label_resize_shape, preserve_range=True).astype(np.uint8)
            label = label.astype(np.float32)

        label = label.astype(np.float32)
        print(label.shape)
        label = np.argmax(label, axis=-1)
        plt.imshow(label)
        plt.show()


if __name__ == "__main__":
    label = "E:\\ISEF\\VHSCDD\\files\\masks\\heartmaskencode0-slice145_saggital.npy"
    encoding_check(label=label)
