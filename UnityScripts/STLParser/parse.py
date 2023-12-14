import meshio
import numpy as np
import sys
import os


def recenter_mesh(mesh):
    offset = -np.mean(mesh.points, axis=0)
    mesh.points = mesh.points + offset


def main(path, is_file: bool = True):
    if is_file:
        stl_to_obj(path)
    else:
        stl_to_obj_dir(path)


def stl_to_obj(path):
    obj_file_path = "E://ISEF//VascuIAR//UnityScripts//STLParser//output_file.obj"

    print(path)
    mesh = meshio.read(path)
    newMesh = meshio.Mesh(mesh.points, mesh.cells)
    # recenter_mesh(newMesh)

    meshio.write(obj_file_path, newMesh)


def stl_to_obj_dir(dir_path):
    for file in os.listdir(dir_path):
        if file.split["."][-1] == "stl":
            pass
        else:
            continue


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print(
            f"Error, program expects 1 command line argument of type str, but received {len(args) - 1} instead.")
        sys.exit()

    path = args[1]
    if os.path.isfile(path):
        main(path, True)
    elif os.path.isdir(path):
        main(path, False)


# ['E:\\ISEF\\VascuIAR\\UnityScripts\\STLParser\\parse.py',
# 'C:/Users/Acer/Downloads/ct_0096_label.nii/label_6_myocardium.stl']
