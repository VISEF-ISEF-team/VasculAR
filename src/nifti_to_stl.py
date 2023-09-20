import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure

# Path to the nifti file (.nii, .nii.gz)
file_path = "../data/3D/test.nii.gz"

# Extract the numpy array
nifti_file = nib.load(file_path)
np_array = nifti_file.get_fdata()

verts, faces, normals, values = measure.marching_cubes(np_array, 0)
obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(faces):
    obj_3d.vectors[i] = verts[f]

# Save the STL file with the name and the path
obj_3d.save('3d_seg_nii_to_stl_test.stl')