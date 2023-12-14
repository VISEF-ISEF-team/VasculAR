using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;
using static UnityEditor.Rendering.CameraUI;
using System.Net.Sockets;

[Serializable]
class TestMeshData
{
    public int[] triangles;
    public Vector3[] vertices; 
}

[Serializable] 
class CustomMesh
{
    public int[] triangles; 
    public Vector3[] vertices; 
}
public class STLParserTest : MonoBehaviour
{
    private string jsonContent;
    public bool DoIt = false;
    private MeshFilter meshFilter;
    private Mesh mesh;
    private float scaleFactor = 0.01f; 

    private void Start()
    {
        meshFilter = GetComponent<MeshFilter>();
        mesh = new Mesh(); 
    }
    private void Update()
    {
        if (DoIt)
        {
            jsonContent = File.ReadAllText(@"E:\ISEF\VascuIAR\UnityScripts\STLParser\vertices.json");
            TestMeshData testMeshData = JsonUtility.FromJson<TestMeshData>(jsonContent);
            
            for (int i = 0; i < testMeshData.vertices.Length; i++) 
            {
                testMeshData.vertices[i] = testMeshData.vertices[i] * scaleFactor;
            }

            mesh.vertices = testMeshData.vertices;  
            mesh.triangles = testMeshData.triangles;
            meshFilter.mesh = mesh; 

            DoIt = false; 
        }
    }
}
