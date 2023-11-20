import vedo
from vedo.applications import IsosurfaceBrowser
import SimpleITK as sitk
import numpy as np
from vedo.applications import FreeHandCutPlotter


# Load NIfTI file using SimpleITK
nifti_image = sitk.ReadImage('D:/Documents/GitHub/VascuIAR/DeepLearning/data/MM_WHS/train_images/ct_train_1017_image.nii.gz')

# Convert to NumPy array
array = sitk.GetArrayFromImage(nifti_image)

# Create a Vedo volume from the array
vol = vedo.Volume(array) 

# IsosurfaceBrowser(Plotter) instance:
plt = IsosurfaceBrowser(vol, use_gpu=True, c='copper')

plt.show(axes=0, bg='black').close()