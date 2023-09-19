import pydicom as dicom
import matplotlib.pyplot as plt

path = "../data/dicom/PAT034/D0024.dcm"
slice = dicom.dcmread(path)
print(dir(slice))
print(slice)
print(slice.PatientName)
plt.imshow(slice.pixel_array, cmap=plt.cm.gray)
plt.show()
