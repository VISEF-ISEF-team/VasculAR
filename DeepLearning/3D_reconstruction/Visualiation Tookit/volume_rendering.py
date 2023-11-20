import pyvista as pv

# Load medical volume data (replace 'your_volume.nii' with your actual file)
volume = pv.read('D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0014_label_resized/ct_0014_label_12.nii.gz')

# Create a PyVista plotter
plotter = pv.Plotter()

# Add the volume to the plotter
plotter.add_volume(volume)

# Show the plot
plotter.show()

# Plot slices of the volume
volume.plot_slices(interactive=True)

# Plot contours
contours = volume.contour()
contours.plot()