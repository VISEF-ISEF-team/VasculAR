import numpy as np
import _bit_marching_cubes_lorensen_cy
from stl import mesh
import time

x_dim = y_dim = z_dim = 500
x = np.linspace(-250, 250, x_dim)
y = np.linspace(-250, 250, y_dim)
z = np.linspace(-250, 250, z_dim)
x, y, z = np.meshgrid(x, y, z)

level = 300
volume = np.sqrt(x**2 + y**2 + z**2).astype(np.float32)
mask = np.asarray(volume >= level, dtype="bool").astype(int)
# cube = np.array([[[0.0] * (250 - 1) for _ in range(250 - 1)] for _ in range(250 - 1)]).astype(np.float32)


start_time = time.time()
verts, faces, vol_, sum_ = _bit_marching_cubes_lorensen_cy.MarchingCubesLorensen(volume, mask, level)
end_time = time.time()

# verts = np.array(verts)
# faces = np.array(faces)

# obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
# for i, f in enumerate(faces):
#     obj_3d.vectors[i] = verts[f]
    
# obj_3d.save('sphere.stl')

print(end_time - start_time)
print(vol_)
print(sum_)


