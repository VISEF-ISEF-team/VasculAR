import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import load, Volume, show
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk

def reconstruction(file_path, index_class):
    # Extract the numpy array
    nifti_file = nib.load(file_path)
    np_array = nifti_file.get_fdata()

    verts, faces, normals, values = measure.marching_cubes(np_array, 0)
    obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        obj_3d.vectors[i] = verts[f]

    # Save the STL file with the name and the path
    obj_3d.save('res_recon/cardiac_' + str(index_class + 1) + '.stl')
    
def run():
    # Path to the nifti file (.nii, .nii.gz)
    file_path = next(os.walk("res"))[2]

    for index_class, value in enumerate(file_path):
        reconstruction(file_path='res/' + file_path[index_class], index_class=index_class)

    mesh = load("res_recon/cardiac_1.stl").color('red').smooth(niter=100)
    mesh1 = load("res_recon/cardiac_2.stl").color('blue').smooth(niter=100)


    # Show the smoothed meshes
    show(mesh, mesh1, bg="black")

def reconstruction_full(file_path):
    # Extract the numpy array
    nifti_file = nib.load(file_path)
    np_array = nifti_file.get_fdata()

    verts, faces, normals, values = measure.marching_cubes(np_array, 0)
    obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        obj_3d.vectors[i] = verts[f]

    # Save the STL file with the name and the path
    obj_3d.save('res_recon_full/cardiac_full.stl')

def run_full():
    reconstruction_full(file_path='res_full/ct_train_1001_label.nii.gz')
    mesh = load("res_recon_full/cardiac_full.stl").smooth(niter=100)
    show(mesh, bg="black")
    

def segmented_reconstruction(file_path):
    whole_heart = sitk.ReadImage(file_path, sitk.sitkFloat32)
    whole_heart = sitk.GetArrayFromImage(whole_heart)
    
    whole_heart_flattened = whole_heart.flatten()
    unique_values, counts = np.unique(whole_heart_flattened, return_counts=True)
    
    label_arrays = []

    # Loop through the unique values
    for value in unique_values: 
        label_array = np.copy(whole_heart) 
        label_array[np.where(label_array != value)] = 0 
        label_arrays.append(label_array)

    # Loop through classes and create mesh
    for i, label_array in enumerate(label_arrays): 
        # background
        if i == 0:
            continue
        
        verts, faces, normals, values = measure.marching_cubes(label_arrays[i], 0)
        obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        
        for j, f in enumerate(faces):
            obj_3d.vectors[j] = verts[f]

        # Save the STL file with the name and the path
        obj_3d.save(f'res_recon_full_seg/cardiac_class_{i}.stl')
        
        
    # Load mesh and display reconstructed 3D with different colors
    mesh1 = load("res_recon_full_seg/cardiac_class_1.stl").color('red').smooth(niter=100)
    mesh2 = load("res_recon_full_seg/cardiac_class_2.stl").color('green').smooth(niter=100)
    mesh3 = load("res_recon_full_seg/cardiac_class_3.stl").color('blue').smooth(niter=100)
    mesh4 = load("res_recon_full_seg/cardiac_class_4.stl").color('yellow').smooth(niter=100)
    mesh5 = load("res_recon_full_seg/cardiac_class_5.stl").color('magenta').smooth(niter=100)
    mesh6 = load("res_recon_full_seg/cardiac_class_6.stl").color('cyan').smooth(niter=100)
    mesh7 = load("res_recon_full_seg/cardiac_class_7.stl").color('white').smooth(niter=100)

    show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, bg="black")
    
    
segmented_reconstruction("loss_function/ct_train_1001_label.nii.gz")