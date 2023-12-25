import meshio
import numpy as np
import sys
import os
import re
import multiprocessing


def recenter_mesh(mesh):
    offset = -np.mean(mesh.points, axis=0)
    mesh.points = mesh.points + offset


def main(path, is_file: bool = True):
    if is_file:
        stl_to_obj(path)
    else:
        stl_to_obj_dir_base_function(path)


def stl_to_obj(path, output_path="E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\output_file.obj"):
    print(path)
    mesh = meshio.read(path)
    newMesh = meshio.Mesh(mesh.points, mesh.cells)

    meshio.write(output_path, newMesh)


def stl_to_obj_with_recenter(path,  output_path="E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\output_file.obj"):
    print(path)
    mesh = meshio.read(path)
    newMesh = meshio.Mesh(mesh.points, mesh.cells)
    recenter_mesh(newMesh)

    meshio.write(output_path, newMesh)


def stl_to_obj_dir_with_recenter(processed_dir_path: list):
    print("called dir with recenter function")
    # C:\Users\Acer\Downloads\ct_0096_label.nii\label_2_left_ventricle.stl

    obj_folder_path = "E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\obj_folder\\"
    obj_file_name_list = []
    vertices_list = []
    cell_list = []
    for file in processed_dir_path:
        mesh = meshio.read(file)
        path_split = file.split(".")[1]
        path_split = path_split.split("_")

        # generate obj file name accordingly
        filename = ""
        if len(path_split) > 3:
            filename += path_split[2]
            filename += "_"
            filename += path_split[3]
        elif len(path_split) == 3:
            filename = path_split[2]
        obj_file_name_list.append(
            f"{os.path.join(obj_folder_path, filename)}.obj")
        vertices_list.append(mesh.points)
        cell_list.append(mesh.cells)

    all_vertices = np.concatenate(vertices_list, axis=0)
    centroid = -np.mean(all_vertices, axis=0)

    del all_vertices

    # recenter mesh by adjusting position according to centroid
    recentered_vertices_list = [vert + centroid for vert in vertices_list]

    counter = 0
    for recentered_vertices, current_cell in zip(recentered_vertices_list, cell_list):
        newMesh = meshio.Mesh(recentered_vertices, current_cell)
        meshio.write(obj_file_name_list[counter], newMesh)
        counter += 1

    del vertices_list
    del recentered_vertices_list
    del cell_list
    del newMesh


def stl_to_obj_dir_base_function(dir_path):
    def extract_numeric_part(file_name):
        matches = re.findall(r'\d+', file_name)
        return [int(match) for match in matches]

    print("called dir function")

    stl_path_list = []
    for file in os.listdir(dir_path):
        if get_file_extension(file):
            stl_path_list.append(os.path.join(dir_path, file))

    stl_path_list = sorted(
        stl_path_list, key=extract_numeric_part)

    stl_to_obj_dir_with_recenter(stl_path_list)


def get_file_extension(file_path):
    return file_path.split(".")[-1] == "stl"


# worker function for reading stl files and add vertices + cells into list for recentering
def worker_read_mesh_function(file: str, obj_file_name_list: list, obj_folder_path: str, vertices_list: list, cell_list: list, lock: multiprocessing.Lock):
    """file: string - a path of an stl file in the whole directory"""
    mesh = meshio.read(file)
    path_split = file.split("label_")[-1].split("_")

    # generate obj file name accordingly
    filename = ""
    if len(path_split) == 3:
        # pulmonary _ trunk
        secondary_organ_name = path_split[-1].split(".")[0]
        filename += path_split[1]
        filename += "_"
        filename += secondary_organ_name
    elif len(path_split) == 2:
        secondary_organ_name = path_split[-1].split(".")[0]
        filename = secondary_organ_name

    with lock:
        obj_file_name_list.append(
            f"{os.path.join(obj_folder_path, filename)}.obj")

        vertices_list.append(mesh.points)
        cell_list.append(mesh.cells)


# worker function for writing mesh to obj file


def worker_write_mesh_function(vert_and_cell_index: int, obj_file_name_list_counter: int, recentered_vertices_list: list, cell_list: list, obj_file_name_list: list):
    """
    vert_and_cell_index: the index for vertices_list and cell_list
    obj_file_name_list_counter: the index for obj_file_name_list
    """
    newMesh = meshio.Mesh(
        recentered_vertices_list[vert_and_cell_index], cell_list[vert_and_cell_index])
    meshio.write(obj_file_name_list[obj_file_name_list_counter], newMesh)


def stl_to_obj_dir_with_parralel_processing(dir_path):
    def extract_numeric_part(file_name):
        matches = re.findall(r'\d+', file_name)
        return [int(match) for match in matches]

    print("called dir function")

    stl_path_list = []
    for file in os.listdir(dir_path):
        if get_file_extension(file):
            stl_path_list.append(os.path.join(dir_path, file))

    stl_path_list = sorted(
        stl_path_list, key=extract_numeric_part)

    # stl_to_dir_with_recenter
    obj_folder_path = "E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\obj_folder\\"
    obj_file_name_list = multiprocessing.Manager().list()
    vertices_list = multiprocessing.Manager().list()
    cell_list = multiprocessing.Manager().list()
    mesh_read_processes = []
    mesh_write_processes = []
    lock = multiprocessing.Lock()

    for file in stl_path_list:
        process = multiprocessing.Process(
            target=worker_read_mesh_function, args=(file, obj_file_name_list, obj_folder_path, vertices_list, cell_list, lock))
        mesh_read_processes.append(process)

    for process in mesh_read_processes:
        process.start()

    for process in mesh_read_processes:
        process.join()

    # calculate total offset for each mesh
    all_vertices = np.concatenate(vertices_list, axis=0)
    centroid = -np.mean(all_vertices, axis=0)

    # calculate recentered vertices
    recentered_vertices_list = [vert + centroid for vert in vertices_list]

    counter = 0
    for i in range(len(recentered_vertices_list)):
        process = multiprocessing.Process(
            target=worker_write_mesh_function, args=(i, counter, recentered_vertices_list, cell_list, obj_file_name_list))
        mesh_write_processes.append(process)
        counter += 1

    for process in mesh_write_processes:
        process.start()

    for process in mesh_write_processes:
        process.join()


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
        stl_to_obj_dir_with_parralel_processing(path)


# ['E:\\ISEF\\VascuIAR\\UnityScripts\\STLParser\\parse.py',
# 'C:/Users/Acer/Downloads/ct_0096_label.nii/label_6_myocardium.stl']
