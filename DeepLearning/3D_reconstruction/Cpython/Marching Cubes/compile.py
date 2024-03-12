import SimpleITK as sitk
import numpy as np
from stl import mesh
import _bit_marching_cubes_lorensen_cy
import time

path = "D:\Documents\GitHub\VascuIAR\DeepLearning\data\VnRawData\VHSCDD_sep_labels\VHSCDD_020_label\ct_020_label_12.nii.gz"
raw = sitk.ReadImage(path, sitk.sitkFloat32)
volume = sitk.GetArrayFromImage(raw)

level = 0.5
mask = np.asarray(volume >= level, dtype="bool").astype(int)
# cube = np.array([[[0.0] * (volume.shape[2] - 1) for _ in range(volume.shape[1] - 1)] for _ in range(volume.shape[0] - 1)]).astype(np.float32)


start_time = time.time()
verts, faces, fenwick, sum_ = _bit_marching_cubes_lorensen_cy.MarchingCubesLorensen(volume, mask, level)
end_time = time.time()

# verts = np.array(verts)
# faces = np.array(faces)

# obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
# for i, f in enumerate(faces):
#     obj_3d.vectors[i] = verts[f]
    
# obj_3d.save('coronary.stl')

print(end_time - start_time)
print(fenwick.getSum(volume.shape[0] - 1, volume.shape[1] - 1, volume.shape[2] - 1))
print(sum_)