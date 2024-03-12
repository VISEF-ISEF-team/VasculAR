from vedo import *

# Load the mesh
mesh = load('coronary.stl')

mesh = mesh.smooth(niter=30,
	pass_band=0.1,
	edge_angle=15,
	feature_angle=60,
	boundary=False)
show(mesh)