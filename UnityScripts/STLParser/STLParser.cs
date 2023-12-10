using UnityEngine;
using System.IO;
using System.Collections.Generic;

public class STLParser : MonoBehaviour
{
    public string stlFilePath = "path/to/your/file.stl"; // Replace with the path to your STL file

    void Start()
    {
        ParseSTLFile();
    }

    private void ParseSTLFile()
    {
        try
        {
            using (FileStream fileStream = new FileStream(stlFilePath, FileMode.Open, FileAccess.Read))
            using (BinaryReader reader = new BinaryReader(fileStream))
            {
                // Read the header (80 bytes, typically ignored)
                byte[] header = reader.ReadBytes(80);

                // Read the number of triangles (4 bytes)
                uint numberOfTriangles = reader.ReadUInt32();

                // Read each triangle
                for (int i = 0; i < numberOfTriangles; i++)
                {
                    // Read normal vector (12 bytes)
                    float normalX = reader.ReadSingle();
                    float normalY = reader.ReadSingle();
                    float normalZ = reader.ReadSingle();

                    // Read vertices (3 vertices, each with X, Y, Z - 36 bytes)
                    Vector3 vertex1 = new Vector3(reader.ReadSingle(), reader.ReadSingle(), reader.ReadSingle());
                    Vector3 vertex2 = new Vector3(reader.ReadSingle(), reader.ReadSingle(), reader.ReadSingle());
                    Vector3 vertex3 = new Vector3(reader.ReadSingle(), reader.ReadSingle(), reader.ReadSingle());

                    // Read attribute byte count (2 bytes, typically ignored)
                    ushort attributeByteCount = reader.ReadUInt16();

                    // Now, you can use the extracted data (e.g., create meshes, visualize, etc.)
                    Debug.Log($"Triangle {i + 1}: Normal ({normalX}, {normalY}, {normalZ}), Vertices: {vertex1}, {vertex2}, {vertex3}");
                }
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError("Error parsing STL file: " + e.Message);
        }
    }
}
