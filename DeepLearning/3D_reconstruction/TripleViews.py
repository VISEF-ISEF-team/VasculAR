from vedo import dataurl, Volume, Text2D
from vedo.applications import Slicer3DPlotter

# Replace 'your_nifti_file.nii.gz' with the actual path to your NIfTI file
nifti_file_path = 'D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_full_labels/ct_020_label.nii.gz'

# Load the NIfTI file as a Volume
vol = Volume(nifti_file_path)

plt = Slicer3DPlotter(
    vol,
    cmaps=("gist_ncar_r", "jet", "Spectral_r", "hot_r", "bone_r"),
    use_slider3d=False,
    bg="black",
)

# Can now add any other vedo object to the Plotter scene:
# plt += Text2D(__doc__)

plt.show(viewup='z')
plt.close()
