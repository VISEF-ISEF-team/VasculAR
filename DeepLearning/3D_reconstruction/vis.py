import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import load, Volume, show, Plotter
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
    
# Define a function to load and smooth a mesh from a file
def load_mesh(filename, color):
    # Load the mesh from the file
    mesh = load(filename)
    # Set the color of the mesh
    mesh.color(color)
    # Smooth the mesh with 100 iterations
    mesh.smooth(niter=100)
    # Return the mesh object
    return mesh


    
def show_mesh():
    # Define a function that toggles the transparency of a mesh and changes the button state
    def buttonfunc1():
        mesh1.alpha(1 - mesh1.alpha())  
        bu1.switch()                  
    def buttonfunc2():
        mesh2.alpha(1 - mesh2.alpha())  
        bu2.switch()
    def buttonfunc3():
        mesh3.alpha(1 - mesh3.alpha())  
        bu3.switch()
    def buttonfunc4():
        mesh4.alpha(1 - mesh4.alpha())  
        bu4.switch()
    def buttonfunc5():
        mesh5.alpha(1 - mesh5.alpha())  
        bu5.switch()
    def buttonfunc6():
        mesh6.alpha(1 - mesh6.alpha())  
        bu6.switch()
    def buttonfunc7():
        mesh7.alpha(1 - mesh7.alpha())  
        bu7.switch()
        

    # Load the meshes from the files and assign different colors
    mesh1 = load_mesh("res_recon_full_seg/cardiac_class_1.stl", "#800000")
    mesh2 = load_mesh("res_recon_full_seg/cardiac_class_2.stl", "#FF8080")
    mesh3 = load_mesh("res_recon_full_seg/cardiac_class_3.stl", "#FFA500")
    mesh4 = load_mesh("res_recon_full_seg/cardiac_class_4.stl", "#800080")
    mesh5 = load_mesh("res_recon_full_seg/cardiac_class_5.stl", "#FF0000")
    mesh6 = load_mesh("res_recon_full_seg/cardiac_class_6.stl", "#FFC0CB")
    mesh7 = load_mesh("res_recon_full_seg/cardiac_class_7.stl", "#0000FF")    

    # Create an instance of the Plotter class with axes style-11 enabled
    plt = Plotter()

    # Add a button to the plotter with buttonfunc as the callback function
    bu1 = plt.add_button(
        buttonfunc1,
        pos=(0.1, 0.05),  # x,y fraction from bottom left corner
        states=["Tam that phai", "Tam that phai"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )

    bu2 = plt.add_button(
        buttonfunc2,
        pos=(0.23, 0.05),  # x,y fraction from bottom left corner
        states=["Tam nhi trai", "Tam nhi trai"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )


    bu3 = plt.add_button(
        buttonfunc3,
        pos=(0.37, 0.05),  # x,y fraction from bottom left corner
        states=["Co tam that trai", "Co tam that trai"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )


    bu4 = plt.add_button(
        buttonfunc4,
        pos=(0.51, 0.05),  # x,y fraction from bottom left corner
        states=["Tam nhi phai", "Tam nhi phai"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )


    bu5 = plt.add_button(
        buttonfunc5,
        pos=(0.64, 0.05),  # x,y fraction from bottom left corner
        states=["Tam that trai", "Tam that trai"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )


    bu6 = plt.add_button(
        buttonfunc6,
        pos=(0.77, 0.05),  # x,y fraction from bottom left corner
        states=["Dong mach chu", "Dong mach chu"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )

    bu7 = plt.add_button(
        buttonfunc7,
        pos=(0.9, 0.05),  # x,y fraction from bottom left corner
        states=["Dong mach phoi", "Dong mach phoi"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )


    # Show the mesh, docstring, and button in the plot
    plt.show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, bg='black')

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
    show_mesh()
    
    
# segmented_reconstruction("loss_function/ct_train_1001_label.nii.gz")
show_mesh()