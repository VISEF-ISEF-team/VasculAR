from stl import mesh
import json
import numpy as np


def STLToJson(stl_file_path: str, json_file_path: str = "vertices.json"):
    """
    STL File Path: path to the stl file that will be called by outer function
    Json File Path: path to write vertices and triangles 
    """
    meshVar = mesh.Mesh.from_file(stl_file_path)
    # vertices: int, key : tuple(float). Int: order of the vertex, list: (x, y, z) representing x, y, z coordinates
    verticesDictionary = {}
    vertexCounter = 0
    # array of ints
    triangleList = list()

    for i, triangles in enumerate(meshVar.vectors):
        for vertices in triangles:
            coordinates = (round(vertices[0], 1), round(
                vertices[1], 1), round(vertices[2], 1))
            if verticesDictionary.get(coordinates) == None:
                verticesDictionary[coordinates] = vertexCounter
                triangleList.append(vertexCounter)
                vertexCounter += 1
            else:
                triangleList.append(verticesDictionary[coordinates])

    sorted_dict_asc = dict(
        sorted(verticesDictionary.items(), key=lambda item: item[1]))

    jsondata = {"triangles": triangleList}
    jsonvertices = []
    for key, value in sorted_dict_asc.items():
        x, y, z = key
        x = float(x)
        y = float(x)
        z = float(z)

        x = round(x, 1)
        y = round(y, 1)
        z = round(z, 1)

        newCooridnates = {
            "x": x,
            "y": y,
            "z": z,
        }
        jsonvertices.append(newCooridnates)

    jsondata["vertices"] = jsonvertices

    with open(json_file_path, "w") as json_file:
        json.dump(jsondata, json_file, indent=4)


def parse_stl(stl_file_path="C://Users//Acer//Downloads//ct_0096_label.nii//label_9_ascending_aorta.stl", json_file_path="vertices.json"):
    mesh_data = mesh.Mesh.from_file(stl_file_path)

    # Extract vertices and triangles
    vertices = mesh_data.vectors.reshape((-1, 3)).tolist()
    triangles = np.arange(len(vertices)).tolist()
    jsonData = {}
    jsonData["triangles"] = triangles
    jsonVertices = []
    for i, vertex in enumerate(vertices):
        coordinates = {
            "x": vertex[0],
            "y": vertex[1],
            "z": vertex[2],
        }
        jsonVertices.append(coordinates)
    jsonData["vertices"] = jsonVertices

    with open(json_file_path, "w") as f:
        json.dump(jsonData, f, indent=4)


def custom_parse_stl(stl_file_path="C://Users//Acer//Downloads//ct_0096_label.nii//label_8_pulmonary_trunk.stl", json_file_path="vertices.json", normal_json_path="normals.json"):
    jsonData = {}
    triangleList = []
    vertexList = []
    normalsList = []
    vertexCounter = 0
    mesh_data = mesh.Mesh.from_file(stl_file_path)

    print(mesh_data.faces)

    # for triangles in mesh_data.vectors:
    #     for vertex in triangles:
    #         triangleList.append(vertexCounter)
    #         coordinates = {
    #             "x": float(vertex[0]),
    #             "y": float(vertex[1]),
    #             "z": float(vertex[2])
    #         }
    #         vertexList.append(coordinates)
    #         vertexCounter += 1

    # for norm in mesh_data.normals:
    #     coordinates = {
    #         "x": float(norm[0]),
    #         "y": float(norm[1]),
    #         "z": float(norm[2])
    #     }
    #     normalsList.append(coordinates)

    # jsonData["triangles"] = triangleList
    # jsonData["vertices"] = vertexList

    # normalData = {
    #     "normals": normalsList
    # }

    # print(len(normalsList), len(vertexList))

    # with open(json_file_path, "w") as f:
    #     json.dump(jsonData, f, indent=4)

    # with open(normal_json_path, "w") as f:
    #     json.dump(normalData, f, indent=4)


if __name__ == "__main__":
    # STLToJson(
    #     "C://Users//Acer//Downloads//ct_0096_label.nii//label_8_pulmonary_trunk.stl")
    custom_parse_stl()
