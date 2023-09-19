import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import os

path = "../data/dicom/PAT034"
ct_images = os.listdir(path)

slices = [dicom.read_file(path + '/' + s, force=True) for s in ct_images]
# print(len(slices))
slices = sorted(slices, key=lambda x:x.ImagePositionPatient[2])

pixel_spacing = slices[0].PixelSpacing
slices_thickess = slices[0].SliceThickness
print(pixel_spacing, slices_thickess)


axial_aspect_ratio = pixel_spacing[1] / pixel_spacing[0]
sagital_aspect_ratio = pixel_spacing[1] / slices_thickess
coronal_aspect_ratio = slices_thickess / pixel_spacing[0]
print(axial_aspect_ratio, sagital_aspect_ratio, coronal_aspect_ratio)


img_shape = list(slices[0].pixel_array.shape)   # tuple --> list
img_shape.append(len(slices))
print(img_shape)
volume_3d = np.zeros(img_shape)

for index, slice in enumerate(slices):
    slice2D = slice.pixel_array
    volume_3d[:,:,index] = slice2D
    
print(slice2D.shape)
print(volume_3d.shape)


axial = plt.subplot(2,2,1)
plt.title("Axial")
plt.imshow(volume_3d[:,:,img_shape[2]//2])
axial.set_aspect(axial_aspect_ratio)

sagital = plt.subplot(2,2,3)
plt.title("Sagital")
plt.imshow(volume_3d[:,img_shape[1]//2,:])
axial.set_aspect(sagital_aspect_ratio)
plt.imshow()

