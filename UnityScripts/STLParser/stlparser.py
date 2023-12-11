from stl import mesh
import json
import sys
import os


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
            coordinates = (vertices[0], vertices[1], vertices[2])
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
        newCooridnates = [float(x), float(y), float(z)]
        jsonvertices.append(newCooridnates)

    jsondata["vertices"] = jsonvertices

    with open(json_file_path, "w") as json_file:
        json.dump(jsondata, json_file, indent=4)


def main(dir_path: str):
    """A folder path containing all the stl files to construct a mesh"""
    # "E:\MM-PATIENT\SEGMENT RESULT\PAT15\SEGMENTATION RESULT"

    # for f in os.listdir(dir_path):
    #     fullPath = os.path.join(dir_path, f)
    #     if os.path.isfile(fullPath):
    #         if fullPath.split('.')[-1] == "stl":
    #             STLToJson(fullPath, os.path.join("json", jsonDir[jsonCounter]))
    #             jsonCounter += 1
    #     else:
    #         continue

    # experiment with text file loading and load all stl files
    verticesDictionary = dict()
    triangleList = list()
    vertexCounter = 0

    for f in os.listdir(dir_path):
        fullPath = os.path.join(dir_path, f)
        if os.path.isfile(fullPath):
            if fullPath.split('.')[-1] == "stl":
                meshVar = mesh.Mesh.from_file(fullPath)

                for i, triangles in enumerate(meshVar.vectors):
                    for vertices in triangles:
                        coordinates = (vertices[0], vertices[1], vertices[2])
                        if verticesDictionary.get(coordinates) == None:
                            verticesDictionary[coordinates] = vertexCounter
                            triangleList.append(vertexCounter)
                            vertexCounter += 1
                        else:
                            triangleList.append(
                                verticesDictionary[coordinates])
            else:
                continue

    sorted_dict_asc = dict(
        sorted(verticesDictionary.items(), key=lambda item: item[1]))

    writtenVertices = []
    for key in sorted_dict_asc.keys():
        x, y, z = key
        newCooridnates = [float(x), float(y), float(z)]
        writtenVertices.append(newCooridnates)

    with open("vertices.txt", "w", encoding="utf-8") as f:
        f.write("Triangles\n")
        for triangle in triangleList:
            f.write(f"{triangle}\n")

        f.write("Vertices\n")
        for vertex in writtenVertices:
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")

    # about 2.4 million different vertices => too excessive, may need to reconsider or reconstruct differently in Unity


if __name__ == "__main__":
    script_name = sys.argv[0]
    arguments = sys.argv[1:]
    if len(arguments) > 1:
        sys.exit(
            "Expect 1 command line argument of type string but received 2")
    path = arguments[0]
    if path.split('.')[-1] == "stl":
        STLToJson(path)
    else:
        main(path)
