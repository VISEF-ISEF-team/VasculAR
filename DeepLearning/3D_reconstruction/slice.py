from vedo import load, dataurl, Text2D
from vedo.applications import Slicer3DPlotter


# Load NIfTI file
nifti_file = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/MM_WHS/train_images/ct_train_1017_image.nii.gz"
vol = load(nifti_file)

plt = Slicer3DPlotter(
    vol,
    cmaps=("gist_ncar_r", "jet", "Spectral_r", "hot_r", "bone_r"),
    use_slider3d=False,
    bg="black",
    bg2="black",
)

# Can now add any other vedo object to the Plotter scene:
plt += Text2D("Use sliders to slice a Volume (click button to change colormap)")

plt.show(bg='black', viewup='z')
plt.close()
