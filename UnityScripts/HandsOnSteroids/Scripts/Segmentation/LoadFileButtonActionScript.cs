using UnityEditor;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using Dummiesman;
using System.IO;

public class LoadFileButtonActionScript : MonoBehaviour
{
    [SerializeField] Material newMaterial;
    [SerializeField] GameObject parentObject;
    private MeshRenderer childMeshRenderer;
    private GameObject loadedObject; 

    private bool coroutineError = false;

    private float scaleFactor = 0.007f;

    private void Update()
    {
        if (coroutineError)
        {
            StopCoroutine(LoadFileCoroutine()); 
        }
    }

    public void LoadFile()
    {
        StartCoroutine(LoadFolderCoroutine());    
    }

    private IEnumerator LoadFileCoroutine()
    {
        string interpreterPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\.venv\\Scripts\\python.exe";
        string parserFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\parse.py";
        string objFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\output_file.obj";

        string stlFilePath = UnityEditor.EditorUtility.OpenFilePanel("Select STl file", "", "");

        UnityEngine.Debug.Log(stlFilePath); 

        yield return null;

        if (!string.IsNullOrEmpty(stlFilePath))
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo()
            {
                FileName = interpreterPath,
                Arguments = $"{parserFilePath} {stlFilePath}",
                RedirectStandardError = true,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };

            using (Process process = new Process { StartInfo = processStartInfo })
            {
                process.Start();
                process.WaitForExit();
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                
                if (!string.IsNullOrEmpty(error))
                {
                    UnityEngine.Debug.Log("Python Script Error:");
                    UnityEngine.Debug.Log(error);
                    coroutineError = true;
                    StopCoroutine(LoadFileCoroutine());
                }
                else if (!string.IsNullOrEmpty(output)) 
                {
                    UnityEngine.Debug.Log(output);
                    coroutineError = true;
                }

                string loadedObjectName = ""; 
                string[] parsedName = Path.GetFileNameWithoutExtension(stlFilePath).Split("_"); 

                if (parsedName.Length > 3)
                {
                    for (int i = 2; i < parsedName.Length; i++)
                    {
                        loadedObjectName += parsedName[i];
                        loadedObjectName += " "; 
                    }
                }
                else if (parsedName.Length == 3) 
                {
                    loadedObjectName = parsedName[2];
                }
                else
                {
                    loadedObjectName = Path.GetFileNameWithoutExtension(stlFilePath);
                }

                loadedObject = new OBJLoader().Load(objFilePath);
                loadedObject.name = loadedObjectName;
                loadedObject.transform.position = Vector3.zero;
                loadedObject.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);
                childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>(); 
                childMeshRenderer.material = newMaterial;

                loadedObject.transform.SetParent(parentObject.transform, false); 
            }
        }
        else
        {
            coroutineError = true;
            yield return null;
        }
    }

    private IEnumerator LoadFolderCoroutine()
    {
        string interpreterPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\.venv\\Scripts\\python.exe";
        string parserFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\parse.py";
        string objFolderPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\\obj_folder\\";

        string stlFolderPath = UnityEditor.EditorUtility.OpenFolderPanel("Select STL folder", "", "");

        yield return null; 

        if (!string.IsNullOrEmpty(stlFolderPath))
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo()
            {
                FileName = interpreterPath,
                Arguments = $"{parserFilePath} {stlFolderPath}",
                RedirectStandardError = true,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };

            using (Process process = new Process { StartInfo = processStartInfo })
            {
                process.Start();
                process.WaitForExit();
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();


                if (!string.IsNullOrEmpty(error))
                {
                    UnityEngine.Debug.Log("Python Script Error:");
                    UnityEngine.Debug.Log(error);
                    coroutineError = true;
                    StopCoroutine(LoadFileCoroutine());
                }
                else if (!string.IsNullOrEmpty(output))
                {
                    UnityEngine.Debug.Log(output);
                    coroutineError = true;
                }

                string[] objFileList = Directory.GetFiles(objFolderPath);

                // loop through all the file in Object Folder
                foreach (string filePath in objFileList)
                {
                    // initialize object to spawn 
                    string loadedObjectName = Path.GetFileNameWithoutExtension(filePath);
                    GameObject loadedObject; 

                    loadedObject = new OBJLoader().Load(filePath);
                    loadedObject.name = loadedObjectName;
                    loadedObject.transform.position = Vector3.zero;
                    loadedObject.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);
                    childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>();
                    childMeshRenderer.material = newMaterial;

                    loadedObject.transform.SetParent(parentObject.transform, false);
                }
            }
            yield return null; 
        }
        else
        {
            coroutineError = true;
            yield return null;
        }
        yield return null; 
    }
}

