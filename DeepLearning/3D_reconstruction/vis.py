import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import load, Volume, show
from vedo.applications import RayCastPlotter
import os

def reconstruction(file_path, index_class):
    # Extract the numpy array
    nifti_file = nib.load(file_path)
    np_array = nifti_file.get_fdata()

    verts, faces, normals, values = measure.marching_cubes(np_array, 0)
    obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        obj_3d.vectors[i] = verts[f]

    # Save the STL file with the name and the path
    obj_3d.save('res/cardiac_' + str(index_class + 1) + '.stl')
    
def run():
    # Path to the nifti file (.nii, .nii.gz)
    file_path = next(os.walk("res"))[2]

    for index_class, value in enumerate(file_path):
        reconstruction(file_path='res/' + file_path[index_class], index_class=index_class)

    mesh = load("cardiac_1.stl").color('red').smooth(niter=100)
    mesh1 = load("cardiac_2.stl").color('blue').smooth(niter=100)


    # Show the smoothed meshes
    show(mesh, mesh1, bg="black")
