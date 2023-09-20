from vedo import load, Volume, show

path_stl = "assets/3D/output_file.stl"
path_nifti = "../data/dicom/test.nii.gz"

# mesh = load(path_stl)
# show(mesh, bg="black")

mesh  = Volume()
show(mesh)