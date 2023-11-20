import vedo

# Load your STL file
mesh = vedo.load('D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0022_label_resized/label_12_coronary_artery.stl')

# Set parallel projection
vedo.settings.use_parallel_projection = True

# Create a FreeHandCutPlotter
plotter = vedo.applications.FreeHandCutPlotter(mesh)

# Add hover legend
plotter.add_hover_legend()

# Start the interactive cutting plot
plotter.start(axes=1, bg2='lightblue').close()
