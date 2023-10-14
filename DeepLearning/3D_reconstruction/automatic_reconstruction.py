import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import *
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk
from tqdm import tqdm


# Define a function to load and smooth a mesh from a file
def load_mesh(filename, color, texture):
    mesh = load(filename)
    mesh.color(color)
    mesh.smooth(niter=100)
    mesh.texture('textures/' + texture)
    return mesh

def show_mesh(path):
    
    meshes = []
    colors = ['#f1d691', '#b17a65', '#6fb8d2', '#d8654f', '#b17a65', '#b17a65', '#b17a65',  '#fc8184', '#0d05ff', '#e6dc46', '#fa0101', '#f4d631', '#fc8184', '#90ee90', '#0d05ff']
    textures = ['cardiac_texture_4.jpg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg', 'cardiac_texture_3.jpg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg']
    files = [f for f in os.listdir(path) if f.endswith('.stl')]
    buttons = []
    plt = Plotter()

    for i in tqdm(range(len(files))):
        if files[i].endswith('.stl'):
            print(path + files[i])
            mesh = load_mesh(path + files[i], colors[i], textures[i])
            meshes.append(mesh)

            # Define a function to toggle the alpha of a given mesh
            def toggle_alpha(mesh, i):
                def buttonfunc():
                    mesh.alpha(1 - mesh.alpha())  
                    buttons[i].switch()  
                return buttonfunc

            # Add a button for each mesh in meshes
            button = plt.add_button(
                toggle_alpha(mesh, i),
                pos=(0.03, 0.24 - i * 0.02),  # x,y fraction from bottom left corner
                states=[str(i+1), str(i+1)],  # text for each state
                c=["w", "w"],                 # font color for each state
                bc=["#0d6efd", "dv"],         # background color for each state
                font="courier",               # font type
                size=10,                      # font size
                bold=True,                    # bold font
                italic=False,                 # non-italic font style
                angle=0.3,
            )
            
            buttons.append(button)
        
    plt = show(meshes, bg='black')
    plt.show()
    
show_mesh('../data/MM_WHS/seg_res/1006/')