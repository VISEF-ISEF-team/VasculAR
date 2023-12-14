using UnityEditor;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using System.IO;
using System.Collections.Generic;
using System;
using UnityEngine.Rendering;

[System.Serializable]
public class MeshData
{
    public int[] triangles;

    public Vector3[] vertices; 
 
}
public class LoadFileButtonActionScript : MonoBehaviour
{
    [SerializeField] GameObject meshObject;
    [SerializeField] Material meshMaterial;
    private MeshFilter meshFilter;
    private Mesh mesh;
    private string jsonContent;

    private bool coroutineError = false;
    private bool isStartingCoroutine = false;

    private float scaleFactor = 0.001f; 

    private void Start()
    {
        meshFilter = meshObject.GetComponent<MeshFilter>();
        mesh = new Mesh(); 
    }
    private void Update()
    {
        if (coroutineError)
        {
            StopCoroutine(LoadFileCoroutine()); 
        }
    }

    public void LoadFile()
    {
        if (isStartingCoroutine == false)
        {
            StartCoroutine(LoadFileCoroutine());
            isStartingCoroutine = true;
        }
        else
        {
            StopCoroutine(LoadFileCoroutine());
            isStartingCoroutine= false; 
        }
    }

    private IEnumerator LoadFileCoroutine()
    {
        string interpreterPath = @"E:\ISEF\VascuIAR\.venv\Scripts\python.exe";
        string parserFilePath = @"E://ISEF//VascuIAR//UnityScripts//STLParser//stlparser.py";
/*        string jsonDirPath = @"E:\ISEF\VascuIAR\UnityScripts\STLParser\json\";*/
        string jsonFilePath = @"E:\ISEF\VascuIAR\UnityScripts\STLParser\vertices.json";

        string stlFilePath = UnityEditor.EditorUtility.OpenFilePanel("Select STl file", "", "");

        yield return null;

        if (!string.IsNullOrEmpty(stlFilePath))
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo()
            {
                FileName = interpreterPath,
                Arguments = $"\"{parserFilePath}\" \"{stlFilePath}\" \"{jsonFilePath}\"",
                RedirectStandardError = true,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };

            yield return new WaitForSeconds(0.5f);

            using (Process process = new Process { StartInfo = processStartInfo })
            {
                process.Start();
                yield return new WaitForSeconds(2.0f); 
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();
                
                if (!string.IsNullOrEmpty(error))
                {
                    UnityEngine.Debug.Log("Python Script Error:");
                    UnityEngine.Debug.Log(error);
                    coroutineError = true; 
                }
                else if (!string.IsNullOrEmpty(output)) 
                {
                    UnityEngine.Debug.Log(output);
                    coroutineError = true; 
                }
/*                string[] jsonFiles = Directory.GetFiles(jsonDirPath);

                for (int i = 0; i < jsonFiles.Length; ++i)
                {
                    string file = jsonFiles[i]; 
                    string jsonContent = File.ReadAllText(file);
                    MeshData meshData = JsonUtility.FromJson<MeshData>(jsonContent);
                    mesh.vertices = meshData.vertices;
                    mesh.SetTriangles(meshData.triangles, i);

                    yield return new WaitForSeconds(.5f); 
                }*/

                jsonContent = File.ReadAllText(jsonFilePath);
                MeshData meshData = JsonUtility.FromJson<MeshData>(jsonContent);
                yield return new WaitForSeconds(1.0f); 
                for (int i = 0; i < meshData.vertices.Length; ++i)
                {
                    meshData.vertices[i].x = meshData.vertices[i].x * scaleFactor;
                    meshData.vertices[i].y = meshData.vertices[i].y * scaleFactor;
                    meshData.vertices[i].z = meshData.vertices[i].z * scaleFactor;
                }
                mesh.SetVertices(meshData.vertices);
                mesh.SetTriangles(meshData.triangles, 0);
                mesh.RecalculateNormals();
                meshFilter.mesh = mesh;

            }
        }
        else
        {
            coroutineError = true;
            yield return null; 
        }
    }
}

