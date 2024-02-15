import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import skimage.transform as skTrans
import cv2

a = np.load(
    "E://ISEF//VHSCDD//files//masks//heartmaskencode0-slice251_axial.npy")

img = cv2.imread(
    "E://ISEF//VHSCDD//files//images//heart0-slice251_axial.png", cv2.IMREAD_GRAYSCALE)

img = cv2.resize(img, (400, 400))
img = img.astype(np.float32)

cv2.imwrite("resize.png", img)

b = skTrans.resize(a, (400, 400, 12), preserve_range=True).astype(np.uint8)

print(np.unique(b), np.max(b), np.min(b))
print(b)

bmax = np.argmax(b, axis=-1)
plt.imshow(bmax)
plt.show()
