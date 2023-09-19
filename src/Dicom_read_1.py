import pydicom as dicom
import matplotlib.pyplot as plt

path = "../data/dicom/PAT034/D0024.dcm"
slices = dicom.dcmread(path)
print(dir(slices))
print(slices)
plt.imshow(slices.pixel_array, cmap=plt.cm.gray)
plt.show()
