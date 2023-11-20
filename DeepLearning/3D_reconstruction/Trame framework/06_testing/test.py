import pyvista as pv

# Load STL file
stl_file_path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0028_label_resized/label_12_coronary_artery.stl"

# Create PyVista plotter
plotter = pv.Plotter()
# Add STL model
mesh = pv.read(stl_file_path)
plotter.add_mesh(mesh, color="red")

# Show the plot
plotter.show()