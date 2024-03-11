import numpy as np
import _marching_cubes_lorensen_cy
from stl import mesh

x_dim = y_dim = z_dim = 500
x = np.linspace(-25, 25, x_dim)
y = np.linspace(-25, 25, y_dim)
z = np.linspace(-25, 25, z_dim)
x, y, z = np.meshgrid(x, y, z)

level = 25.0
volume = np.sqrt(x**2 + y**2 + z**2).astype(np.float32)
mask = np.asarray(volume >= level, dtype="bool").astype(int)
cube = np.array([[[0.0] * (500 - 1) for _ in range(500 - 1)] for _ in range(500 - 1)]).astype(np.float32)

verts, faces = _marching_cubes_lorensen_cy.MarchingCubesLorensen(volume, mask, cube, level)
verts = np.array(verts)
faces = np.array(faces)

obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    obj_3d.vectors[i] = verts[f]
    
obj_3d.save('sphere.stl')