import numpy 
import sys
import vtk
import glob
import re
import math
from vtk.util import numpy_support as VN


def vtk_intro(input_filename, output_filename, fieldname):
    print("Loading", input_filename)
    reader = vtk.vtkXMLUnstructuredGridReader()
    
    reader.SetFileName(input_filename)
    reader.Update()
    data = reader.GetOutput()
    
    meshToSurf = vtk.vtkDataSetSurfaceFilter() # extract surface
    meshToSurf.SetInputData(data)
    meshToSurf.Update()
    data = meshToSurf.GetOutput()
    
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(data)
    normals.SetFeatureAngle(91)
    normals.SetSplitting(0)
    normals.Update()
    data = normals.GetOutput()
    
    n_points = data.GetNumberOfPoints()
    print('Total of points on surface:', n_points)
    
    # Read arrays in the data, process, and save them
    P = VN.vtk_to_numpy(data.GetPointData().GetArray(fieldname))
    P_dynamic = numpy.zeros((n_points, 1))
    for i in range(n_points):
        P_dynamic[i] = P[i]**2
        
    theta_vtk = VN.numpy_to_vtk(P_dynamic)
    theta_vtk.SetName('P_squared')
    data.GetPointData().AddArray(theta_vtk)
    
    # define a plane for cropping
    plane1 = vtk.vtkPlane()
    plane1.SetOrigin(-3.1,-2.0,-10.9)
    plane1.SetNormal(0.35,-0.25,0.9)
    
    # crop the data with the plane
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputData(data)
    clipper.SetClipFunction(plane1)
    clipper.InsideOutOn() # other side --> clipper.InsiderOutOff()
    data_clipped = clipper.GetOutput()
    
    # process the gradient tensor
    # wss_grad_vector = VN.vtk_to_numpy(data_clipped.GetPointData().GetArray('wssVector_grad'))
    
    # Save the final outcome
    myOutput = vtk.vtkXMLDataSetWriter()
    myOutput.SetInputData(data_clipped)
    myOutput.SetFileName(output_filename)
    myOutput.Write()
    
    print("Sucessfully done")
    
    
    
    
input_filename = 'all_results_10100.vtu'
output_filename = 'cartiod_data_processed.vtk'
fieldname = 'pressure'

vtk_intro(
    input_filename=input_filename,
    output_filename=output_filename,
    fieldname=fieldname
)