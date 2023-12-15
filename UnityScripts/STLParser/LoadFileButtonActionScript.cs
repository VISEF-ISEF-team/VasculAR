using UnityEditor;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using Dummiesman;
using System.IO;
using System.Xml.Serialization;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using JetBrains.Annotations;

public class LoadFileButtonActionScript : MonoBehaviour
{
    [SerializeField] Material newMaterial;
    private MeshRenderer childMeshRenderer;
    private GameObject loadedObject; 

    private bool coroutineError = false;
    private bool isStartingCoroutine = false;

    private float scaleFactor = 0.007f;
    static List<int> ExtractNumericPart(string fileName)
    {
        MatchCollection matches = Regex.Matches(fileName, @"\d+");
        return matches.Cast<Match>().Select(match => int.Parse(match.Value)).ToList();
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
        /*StartCoroutine(LoadFileCoroutine())*/
        ;
        StartCoroutine (LoadFolderCoroutine());
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

        UnityEngine.Debug.Log(stlFolderPath);

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

                // implement loop through folder logic 

                if (Directory.Exists(stlFolderPath))
                {
                    int counter = 1; 

                    // create and sort STL file folder to match the name in obj file 
                    string[] stlFolderPathList = Directory.GetFiles(stlFolderPath);
                    stlFolderPathList = stlFolderPathList.OrderBy(path => ExtractNumericPart(path)).ToArray(); 

                    // loop through all the file in stlFolderPath 
                    foreach (string filePath in Directory.GetFiles(stlFolderPath))
                    {
                        UnityEngine.Debug.Log(filePath);
                        if (filePath.Split(".")[filePath.Split(".").Length - 1] != "stl") continue; 

                        string[] parsedName = Path.GetFileNameWithoutExtension(filePath).Split("_");

                        // initialize object to spawn 
                        string loadedObjectName = ""; 
                        GameObject loadedObject; 

                        // get the name based on the STL file 
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
                            loadedObjectName = Path.GetFileNameWithoutExtension(filePath);
                        }

                        string currentObjFilePath = objFolderPath + $"obj_{counter}.obj";
                        loadedObject = new OBJLoader().Load(currentObjFilePath);
                        loadedObject.name = loadedObjectName;
                        loadedObject.transform.position = Vector3.zero;
                        loadedObject.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);
                        childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>();
                        childMeshRenderer.material = newMaterial;

                        // increment file name counter 
                        counter++; 
                    }
                }
            }
        }
        else
        {
            coroutineError = true;
            yield return null;
        }
        yield return null; 
    }
}

