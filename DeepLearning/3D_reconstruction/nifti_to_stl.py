import SimpleITK as sitk
import numpy as np
from stl import mesh
from skimage import measure

path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels/VHSCDD_020_label/ct_020_label_12.nii.gz"
img_raw = sitk.ReadImage(path, sitk.sitkFloat32)
img = sitk.GetArrayFromImage(img_raw)

verts, faces, normals, values = measure.marching_cubes(img, 0.5)
obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(faces):
    obj_3d.vectors[i] = verts[f]

# Save the STL file with the name and the path
obj_3d.save('coronary.stl')