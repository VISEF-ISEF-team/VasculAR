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
    def buttonfunc8():
        mesh8.alpha(1 - mesh8.alpha())  
        bu8.switch()
    def buttonfunc9():
        mesh9.alpha(1 - mesh9.alpha())  
        bu9.switch()
    def buttonfunc10():
        mesh10.alpha(1 - mesh10.alpha())  
        bu10.switch()    
    def buttonfunc11():
        mesh11.alpha(1 - mesh11.alpha())  
        bu11.switch()  
    def buttonfunc12():
        mesh12.alpha(1 - mesh12.alpha())  
        bu12.switch()  

        # Load the meshes from the files and assign different colors
    mesh1 = load("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_aeorta.stl").color("#fc8184").smooth(niter=100).texture('textures/cardiac_texture_1.jpg')
    mesh2 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_aeortic arch.stl", "#fa0101")
    mesh3 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_bicuspid valve.stl", "#dd8265")
    mesh4 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_IVC.stl", "#e6dc46")
    mesh5 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_left atrium.stl", "#f1d691")
    mesh6 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_left ventricle.stl", "#b17a65")
    mesh7 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_pericardium.stl", "#dcf514")
    mesh8 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_pulmonary artery.stl", "#f4d631")
    mesh9 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_right atrium.stl", "#6fb8d2")
    mesh10 = load("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_right ventricle.stl").color("#d8654f").smooth(niter=100).texture('textures/cardiac_texture_1.jpg')
    mesh11 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_SVC.stl", "#0d05ff")
    mesh12 = load_mesh("../data/PatientsDCM/Segmentation_Result/PAT015/3D_res_3/Segmentation_1_tricuspid valve.stl", "#90ee90")

    # Create an instance of the Plotter class with axes style-11 enabled
    plt = Plotter()

    # Add a button to the plotter with buttonfunc as the callback function
    bu1 = plt.add_button(
        buttonfunc1,
        pos=(0.03, 0.68),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.64),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.60),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.56),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.52),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.48),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.44),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.40),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.36),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.32),  # x,y fraction from bottom left corner
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
        pos=(0.03, 0.28),  # x,y fraction from bottom left corner
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

    # text
    txt1 = Text2D("1: Dong mach chu", pos=(0.02, 0.98), s=0.6, c='white', bold=True)
    txt2 = Text2D("2: Cung dong mach chu", pos=(0.02, 0.96), s=0.6, c='white', bold=True)
    txt3 = Text2D("3: Van hai la", pos=(0.02, 0.94), s=0.6, c='white', bold=True)
    txt4 = Text2D("4: Tinh mach chu duoi", pos=(0.02, 0.92), s=0.6, c='white', bold=True)
    txt5 = Text2D("5: Tam nhi trai", pos=(0.02, 0.90), s=0.6, c='white', bold=True)
    txt6 = Text2D("6: Tam that trai", pos=(0.02, 0.88), s=0.6, c='white', bold=True)
    txt7 = Text2D("7: Mang tim", pos=(0.02, 0.86), s=0.6, c='white', bold=True)
    txt8 = Text2D("8: Dong mach phoi", pos=(0.02, 0.84), s=0.6, c='white', bold=True)
    txt9 = Text2D("9: Tam nhi phai", pos=(0.02, 0.82), s=0.6, c='white', bold=True)
    txt10 = Text2D("10: Tam that phai", pos=(0.02, 0.80), s=0.6, c='white', bold=True)
    txt11 = Text2D("11: Tinh mach chu tren", pos=(0.02, 0.78), s=0.6, c='white', bold=True)
    txt12 = Text2D("12: Van 3 la", pos=(0.02, 0.76), s=0.6, c='white', bold=True)
    
    # Show the mesh, docstring, and button in the plot
    plt = show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, mesh8, mesh9, mesh10, mesh11, mesh12, txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9, txt10, txt11, txt12, bg='black')
    # plt.export('scene.npz')
    plt.show()

show_mesh()
