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
    mesh = load(filename)
    mesh.color(color)
    mesh.smooth(niter=100)
    return mesh

def show_mesh():
    mesh1 = load_mesh("predicted_res/cardiac_class_1.stl", "#fc8184")
    mesh2 = load_mesh("predicted_res/cardiac_class_2.stl", "#fa0101")
    mesh3 = load_mesh("predicted_res/cardiac_class_3.stl", "#dd8265")
    mesh4 = load_mesh("predicted_res/cardiac_class_4.stl", "#e6dc46")
    mesh5 = load_mesh("predicted_res/cardiac_class_5.stl", "#e6dc46")
    
    
    show(mesh1, mesh2, mesh3, mesh4, mesh5, bg='black')
    
show_mesh()