import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import load, Volume, show, Plotter
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk


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
        mesh5.alpha(1 - mesh6.alpha())  
        bu5.switch()
    def buttonfunc7():
        mesh5.alpha(1 - mesh7.alpha())  
        bu5.switch()
    def buttonfunc8():
        mesh5.alpha(1 - mesh8.alpha())  
        bu5.switch()
    def buttonfunc9():
        mesh5.alpha(1 - mesh9.alpha())  
        bu5.switch()
    def buttonfunc10():
        mesh5.alpha(1 - mesh10.alpha())  
        bu5.switch()    
    def buttonfunc11():
        mesh5.alpha(1 - mesh11.alpha())  
        bu5.switch()  
    def buttonfunc12():
        mesh5.alpha(1 - mesh12.alpha())  
        bu5.switch()  
    
        

    # Load the meshes from the files and assign different colors
    mesh1 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_aeorta.stl", "#fc8184")
    mesh2 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_aeortic arch.stl", "#fa0101")
    mesh3 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_bicuspid valve.stl", "#dd8265")
    mesh4 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_IVC.stl", "#e6dc46")
    mesh5 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_left atrium.stl", "#f1d691")
    mesh6 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_left ventricle.stl", "#b17a65")
    mesh7 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_pericardium.stl", "#dcf514")
    mesh8 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_pulmonary artery.stl", "#f4d631")
    mesh9 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_right atrium.stl", "#6fb8d2")
    mesh10 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_right ventricle.stl", "#d8654f")
    mesh11 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_SVC.stl", "#0d05ff")
    mesh12 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_tricuspid valve.stl", "#90ee90")
    

    # Create an instance of the Plotter class with axes style-11 enabled
    plt = Plotter()

    # Add a button to the plotter with buttonfunc as the callback function
    bu1 = plt.add_button(
        buttonfunc1,
        pos=(0.1, 0.05),  # x,y fraction from bottom left corner
        states=["1", "1"],  # text for each state
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
        states=["2", "2"],  # text for each state
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
        states=["3", "3"],  # text for each state
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
        states=["4", "4"],  # text for each state
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
        states=["5", "5"],  # text for each state
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
        pos=(0.7, 0.05),  # x,y fraction from bottom left corner
        states=["6", "T6"],  # text for each state
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
        pos=(0.74, 0.05),  # x,y fraction from bottom left corner
        states=["7", "7"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )
    
    
    bu8 = plt.add_button(
        buttonfunc8,
        pos=(0.78, 0.05),  # x,y fraction from bottom left corner
        states=["8", "8"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )
    
    bu9 = plt.add_button(
        buttonfunc9,
        pos=(0.8, 0.05),  # x,y fraction from bottom left corner
        states=["9", "9"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )
    
    
    bu10 = plt.add_button(
        buttonfunc10,
        pos=(0.84, 0.05),  # x,y fraction from bottom left corner
        states=["10", "10"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )
    
    
    bu11 = plt.add_button(
        buttonfunc11,
        pos=(0.88, 0.05),  # x,y fraction from bottom left corner
        states=["11", "11"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )
    
    
    bu12 = plt.add_button(
        buttonfunc12,
        pos=(0.92, 0.05),  # x,y fraction from bottom left corner
        states=["12", "12"],  # text for each state
        c=["w", "w"],     # font color for each state
        bc=["#0d6efd", "dv"],  # background color for each state
        font="courier",   # font type
        size=10,          # font size
        bold=True,        # bold font
        italic=False,     # non-italic font style
        angle=0.3,
    )



    # Show the mesh, docstring, and button in the plot
    show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, mesh8, mesh9, mesh10, mesh11, mesh12, bg='black')
    
    
show_mesh()