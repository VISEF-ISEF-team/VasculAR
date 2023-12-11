using UnityEditor;
using UnityEngine;
using System;
using System.Diagnostics;
using System.Collections;
using System.IO;

public class LoadFileButtonActionScript : MonoBehaviour
{
    [SerializeField] GameObject meshObject;
    [SerializeField] Material meshMaterial;
    private MeshFilter meshFilter;
    private Mesh mesh; 

    private bool coroutineError = false;
    private bool isStartingCoroutine = false;

    private void Start()
    {
        meshFilter = meshObject.GetComponent<MeshFilter>();
        mesh = meshFilter.mesh; 
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
        }
    }
    struct MeshData
    {
        public int[] triangles;
        public Vector3[] vertices;  
    }
    private IEnumerator LoadFileCoroutine()
    {
        string interpreterPath = @"E:\ISEF\VascuIAR\.venv\Scripts\python.exe";
        string parserFilePath = @"E://ISEF//VascuIAR//UnityScripts//STLParser//stlparser.py";
/*        string jsonDirPath = @"E:\ISEF\VascuIAR\UnityScripts\STLParser\json\";*/
        string jsonFilePath = @"E:\ISEF\VascuIAR\UnityScripts\STLParser\vertices.json";

        string dirPathArg = UnityEditor.EditorUtility.OpenFolderPanel("Select STl file", "", "");

        yield return null;

        if (!string.IsNullOrEmpty(dirPathArg))
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo()
            {
                FileName = interpreterPath,
                Arguments = $"\"{parserFilePath}\" {dirPathArg}",
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

                string jsonContent = File.ReadAllText(jsonFilePath);
                MeshData meshData = JsonUtility.FromJson<MeshData>(jsonContent);
                mesh.vertices = meshData.vertices;
                mesh.triangles = meshData.triangles;
            }
        }
        else
        {
            coroutineError = true;
            yield return null; 
        }
    }
}

