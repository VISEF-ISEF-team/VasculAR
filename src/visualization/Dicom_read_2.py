import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import os

def multi_orientation_viz(path):
    ct_images = os.listdir(path)

    # Read each slice  in dicom folder into slices
    slices = [dicom.read_file(path + '/' + s, force=True) for s in ct_images]
    print("Length of slices (volume):",  len(slices))
    slices = sorted(slices, key=lambda x:x.ImagePositionPatient[2])

    # Get attribute of slices (dicom folder)
    pixel_spacing = slices[0].PixelSpacing
    slices_thickess = slices[0].SliceThickness
    print(f"Pixel spacing: {pixel_spacing} \n Slice thickness: {slices_thickess}")

    # Get three aspect orientation from above attributes
    axial_aspect_ratio = pixel_spacing[1] / pixel_spacing[0]
    sagital_aspect_ratio = pixel_spacing[1] / slices_thickess
    coronal_aspect_ratio = slices_thickess / pixel_spacing[0]
    print(f"Axial aspect ratio: {axial_aspect_ratio} \n Sagital aspect ratio: {sagital_aspect_ratio} \n Coronal aspect ratio: {coronal_aspect_ratio}")

    # Create an 3D array (x,y,z) which is volumetric image
    img_shape = list(slices[0].pixel_array.shape)               # tuple --> list
    img_shape.append(len(slices))
    print("image shape:", img_shape)
    volume_3d = np.zeros(img_shape)

    for index, slice in enumerate(slices):
        slice2D = slice.pixel_array
        volume_3d[:,:,index] = slice2D
    
    print("Slice 2D shape:", slice2D.shape)
    print("Volume 3D shape:", volume_3d.shape)


    # Visualization acording to 3 above ratio
    axial = plt.subplot(2,2,1)
    plt.title("Axial")
    plt.imshow(volume_3d[:,:,img_shape[2]//2])
    axial.set_aspect(axial_aspect_ratio)

    sagital=plt.subplot(2,2,2)
    plt.title("Sagital")
    plt.imshow(volume_3d[:,img_shape[1]//2,:])
    sagital.set_aspect(sagital_aspect_ratio)


    coronal = plt.subplot(2,2,3)
    plt.title("Coronal")
    plt.imshow(volume_3d[img_shape[0]//2,:,:].T)
    coronal.set_aspect(coronal_aspect_ratio)

    plt.show()


# Access the sample patient
all_patients_path = "../data/PatientsDCM/"
patients =  os.listdir(all_patients_path)
patient_01 = all_patients_path + patients[0]

multi_orientation_viz(patient_01)