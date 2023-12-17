using UnityEngine;
using System.IO;
using System;
using System.Linq;

[Serializable]
class TestMeshData
{
    public int[] triangles;
    public Vector3[] vertices; 
}

[Serializable] 
class CustomNormals
{
    public Vector3[] normals; 
}
public class STLParserTest : MonoBehaviour
{
    private string jsonContent;
    public bool DoIt = false;
    private MeshFilter meshFilter;
    private Mesh mesh;
    private MeshRenderer meshRenderer; 

    private void Start()
    {
        meshFilter = GetComponent<MeshFilter>();
        mesh = new Mesh(); 
        meshRenderer = GetComponent<MeshRenderer>();
    }
    private void Update()
    {
        if (DoIt)
        {
            // load data from JSON format   
/*            jsonContent = File.ReadAllText(@"E:\ISEF\VascuIAR\UnityScripts\STLParser\test.json");

            TestMeshData testMeshData = JsonUtility.FromJson<TestMeshData>(jsonContent);
            mesh.listVertices = testMeshData.listVertices;
            mesh.triangleList = testMeshData.triangleList;
            mesh.RecalculateNormals(); 
            mesh.RecalculateBounds();

            Debug.Log(testMeshData.listVertices.Length); 
            Debug.Log(testMeshData.triangleList.Length);   
            meshFilter.mesh = mesh;

            DoIt = false; */
        }
    }
}
