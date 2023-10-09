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
    # def buttonfunc1():
    #     mesh1.alpha(1 - mesh1.alpha())
    #     bu1.switch()
    # def buttonfunc2():
    #     mesh2.alpha(1 - mesh2.alpha())
    #     bu2.switch()
    # def buttonfunc3():
    #     mesh3.alpha(1 - mesh3.alpha())
    #     bu3.switch()
    # def buttonfunc4():
    #     mesh4.alpha(1 - mesh4.alpha())
    #     bu4.switch()
    # def buttonfunc5():
    #     mesh5.alpha(1 - mesh5.alpha())
    #     bu5.switch()

    # Load the meshes from the files and assign different colors
    mesh1 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_aeorta.stl", "#f1d691")
    mesh2 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_aeortic arch.stl", "#b17a65")
    mesh3 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_bicuspid valve.stl", "#6fb8d2")
    mesh4 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_IVC.stl", "#d8654f")
    mesh5 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_left atrium.stl", "#dd8265")
    mesh6 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_left ventricle.stl", "#90ee90")
    mesh7 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_pericardium.stl", "#dcf514")
    mesh8 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_pulmonary artery.stl", "#dcf514")
    mesh9 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_right atrium.stl", "#0d05ff")
    mesh10 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_right ventricle.stl", "#e6dc46")
    mesh11 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_SVC.stl", "#c8c8eb")
    mesh12 = load_mesh(
        "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT\Segmentation_1_tricuspid valve.stl", "#fa0101")

    # # Create an instance of the Plotter class with axes style-11 enabled
    # plt = Plotter()

    # # Add a button to the plotter with buttonfunc as the callback function
    # bu1 = plt.add_button(
    #     buttonfunc1,
    #     pos=(0.1, 0.05),  # x,y fraction from bottom left corner
    #     states=["Tam that phai", "Tam that phai"],  # text for each state
    #     c=["w", "w"],     # font color for each state
    #     bc=["#0d6efd", "dv"],  # background color for each state
    #     font="courier",   # font type
    #     size=10,          # font size
    #     bold=True,        # bold font
    #     italic=False,     # non-italic font style
    #     angle=0.3,
    # )

    # bu2 = plt.add_button(
    #     buttonfunc2,
    #     pos=(0.23, 0.05),  # x,y fraction from bottom left corner
    #     states=["Tam nhi trai", "Tam nhi trai"],  # text for each state
    #     c=["w", "w"],     # font color for each state
    #     bc=["#0d6efd", "dv"],  # background color for each state
    #     font="courier",   # font type
    #     size=10,          # font size
    #     bold=True,        # bold font
    #     italic=False,     # non-italic font style
    #     angle=0.3,
    # )

    # bu3 = plt.add_button(
    #     buttonfunc3,
    #     pos=(0.37, 0.05),  # x,y fraction from bottom left corner
    #     states=["Co tam that trai", "Co tam that trai"],  # text for each state
    #     c=["w", "w"],     # font color for each state
    #     bc=["#0d6efd", "dv"],  # background color for each state
    #     font="courier",   # font type
    #     size=10,          # font size
    #     bold=True,        # bold font
    #     italic=False,     # non-italic font style
    #     angle=0.3,
    # )

    # bu4 = plt.add_button(
    #     buttonfunc4,
    #     pos=(0.51, 0.05),  # x,y fraction from bottom left corner
    #     states=["Tam nhi phai", "Tam nhi phai"],  # text for each state
    #     c=["w", "w"],     # font color for each state
    #     bc=["#0d6efd", "dv"],  # background color for each state
    #     font="courier",   # font type
    #     size=10,          # font size
    #     bold=True,        # bold font
    #     italic=False,     # non-italic font style
    #     angle=0.3,
    # )

    # bu5 = plt.add_button(
    #     buttonfunc5,
    #     pos=(0.64, 0.05),  # x,y fraction from bottom left corner
    #     states=["Tam that trai", "Tam that trai"],  # text for each state
    #     c=["w", "w"],     # font color for each state
    #     bc=["#0d6efd", "dv"],  # background color for each state
    #     font="courier",   # font type
    #     size=10,          # font size
    #     bold=True,        # bold font
    #     italic=False,     # non-italic font style
    #     angle=0.3,
    # )

    # Show the mesh, docstring, and button in the plot
    show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7,
         mesh8, mesh9, mesh10, mesh11, mesh12, bg='black')


show_mesh()
