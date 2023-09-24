from vedo import load, Volume, show

path_stl = "assets/3D/output_file.stl"
path_nifti = "../data/dicom/test.nii.gz"
seg_path = "../data/3D/test.stl"
seg_path_nii = "../data/3D/test.nii.gz"
test_path = "../src/3d_seg_nii_to_stl_test.stl"

mesh1 = load(test_path)
mesh2 = load(seg_path)

show(mesh1, mesh2, bg="black")

# mesh  = Volume(seg_path_nii)
# show(mesh)