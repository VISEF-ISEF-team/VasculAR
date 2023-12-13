from stl import mesh
import numpy as np
import json


from stl import mesh
import numpy as np
import json


def parse_stl_and_save_json(file_path, json_output_path):
    mesh_data = mesh.Mesh.from_file(file_path)
    first = mesh_data.v0
    second = mesh_data.v1
    third = mesh_data.v2

    vertices = []
    triangles = []

    vertex_counter = 0
    for i in range(first.shape[0]):
        v1_coordinate_list = first[i].tolist()
        v1_coordinates = {
            "x": float(v1_coordinate_list[0]) / 100,
            "y": float(v1_coordinate_list[1]) / 100,
            "z": float(v1_coordinate_list[2]) / 100
        }
        triangles.append(vertex_counter)
        vertices.append(v1_coordinates)
        vertex_counter += 1

        v2_coordinate_list = second[i].tolist()
        v2_coordinates = {
            "x": float(v2_coordinate_list[0]) / 100,
            "y": float(v2_coordinate_list[1]) / 100,
            "z": float(v2_coordinate_list[2]) / 100
        }
        triangles.append(vertex_counter)
        vertices.append(v2_coordinates)
        vertex_counter += 1

        v3_coordinate_list = third[i].tolist()
        v3_coordinates = {
            "x": float(v3_coordinate_list[0]) / 100,
            "y": float(v3_coordinate_list[1]) / 100,
            "z": float(v3_coordinate_list[2]) / 100
        }
        triangles.append(vertex_counter)
        vertices.append(v3_coordinates)
        vertex_counter += 1

    jsonData = {
        "triangles": triangles,
        "vertices": vertices
    }

    with open(json_output_path, "w") as f:
        json.dump(jsonData, f, indent=4)


# Example usage
stl_file_path = 'C://Users//Acer//Downloads//ct_0096_label.nii//label_8_pulmonary_trunk.stl'
json_output_path = 'test.json'
parse_stl_and_save_json(stl_file_path, json_output_path)
