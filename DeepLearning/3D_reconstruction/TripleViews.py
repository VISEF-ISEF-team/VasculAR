from vedo import dataurl, Volume, Text2D
from vedo.applications import Slicer3DPlotter

# Replace 'your_nifti_file.nii.gz' with the actual path to your NIfTI file
nifti_file_path = 'intersection.nii'
# Load the NIfTI file as a Volume
vol = Volume(nifti_file_path)

plt = Slicer3DPlotter(
    vol,
    cmaps=("bone_r", "bone_r", "bone_r", "bone_r", "bone_r"),
    use_slider3d=False,
    bg="white",
)

# Can now add any other vedo object to the Plotter scene:
# plt += Text2D(__doc__)

plt.show(viewup='z', bg='white')
plt.close()
