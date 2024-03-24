from vedo import *

path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels/VHSCDD_020_label/"
mesh = load(path + 'label_2_left_ventricle.stl')

print(mesh.points()[:10])
print(mesh.faces()[:10])