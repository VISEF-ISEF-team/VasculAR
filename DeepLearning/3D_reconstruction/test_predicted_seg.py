import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import *
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk



# Define a function to load and smooth a mesh from a file
def load_mesh(filename, color):
    mesh = load(filename)
    mesh.color(color)
    mesh.smooth(niter=100)
    return mesh

def show_mesh():
    mesh1 = load_mesh("MM05/Segmentation_ascending aorta.stl", "#fc8184")
    mesh2 = load_mesh("MM05/Segmentation_left atrium.stl", "#fa0101")
    mesh3 = load_mesh("MM05/Segmentation_descending aorta.stl", "#dd8265")
    mesh4 = load_mesh("MM05/Segmentation_coronary.stl", "#e6dc46")
    mesh5 = load_mesh("MM05/Segmentation_left ventricle.stl", "#f1d691")
    mesh6 = load_mesh("MM05/Segmentation_pulmonary.stl", "#b17a65")
    mesh7 = load_mesh("MM05/Segmentation_right atrium.stl", "#dcf514")
    mesh8 = load_mesh("MM05/Segmentation_right ventricle.stl", "#d8654f")
    mesh9 = load_mesh("MM05/Segmentation_Inferior Vena Cava.stl", "#d8654f")
    mesh10 = load_mesh("MM05/Segmentation_Superior Vena Cava.stl", "#90ee90")
    mesh12 = load_mesh("MM05/Segmentation_Segment_1.stl", "#d8654f")
    
    plt = Plotter()

    def buttonfunc12():
        mesh12.alpha(1 - mesh12.alpha())  
        bu12.switch()  
        
    bu12 = plt.add_button(
            buttonfunc12,
            pos=(0.03, 0.24),  # x,y fraction from bottom left corner
            states=["12", "12"],  # text for each state
            c=["w", "w"],     # font color for each state
            bc=["#0d6efd", "dv"],  # background color for each state
            font="courier",   # font type
            size=10,          # font size
            bold=True,        # bold font
            italic=False,     # non-italic font style
            angle=0.3,
        )


    plt = show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, mesh8, mesh9, mesh10, bg='black')
    plt.show()
    
show_mesh()