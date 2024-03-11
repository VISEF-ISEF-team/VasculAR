import SimpleITK as sitk
import numpy as np
from stl import mesh
import _marching_cubes_lorensen_cy

path = "D:\Documents\GitHub\VascuIAR\DeepLearning\data\VnRawData\VHSCDD_sep_labels\VHSCDD_020_label\ct_020_label_12.nii.gz"
raw = sitk.ReadImage(path, sitk.sitkFloat32)
volume = sitk.GetArrayFromImage(raw)

level = 0.5
mask = np.asarray(volume >= level, dtype="bool").astype(int)
cube = np.array([[[0.0] * (volume.shape[2] - 1) for _ in range(volume.shape[1] - 1)] for _ in range(volume.shape[0] - 1)]).astype(np.float32)

verts, faces = _marching_cubes_lorensen_cy.MarchingCubesLorensen(volume, mask, cube, level)
verts = np.array(verts)
faces = np.array(faces)

obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    obj_3d.vectors[i] = verts[f]
    
obj_3d.save('coronary.stl')