using Dummiesman;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

public class LoadFolderWithJobs : MonoBehaviour
{
    private string interpreterPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\.venv\\Scripts\\python.exe";
    private string parserFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\parse.py";
    private string objFolderPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\\obj_folder\\";
    private string stlFolderPath = @"C:\Users\Acer\Downloads\Base_Folder\ct_0096_label.nii";

    private string parentObjectTag = "Parent Segment Object"; 

    private Dictionary<string, Color> colorDictionary = new Dictionary<string, Color>()
    {
        { "left_ventricle", new Color(241 / 255f, 214 / 255f, 145 / 255f) },
        { "right_ventricle", new Color(216 / 255f, 101 / 255f, 79 / 255f) },
        { "left_atrium", new Color(128 / 255f, 174 / 255f, 128 / 255f) },
        { "right_atrium", new Color(111 / 255f, 184 / 255f, 210 / 255f) },
        { "myocardium",  new Color(220 / 255f, 245 / 255f, 20 / 255f) },
        { "descending_aorta", new Color(250 / 255f, 1 / 255f, 1 / 255f) },
        { "pulmonary_trunk", new Color(244 / 255f, 214 / 255f, 49 / 255f) },
        { "ascending_aorta", new Color(252 / 255f, 129 / 255f, 132 / 255f) },
        { "vena_cava", new Color(13 / 255f, 5 / 255f, 255 / 255f) },
        { "auricle",  new Color(230 / 255f, 220 / 255f, 70 / 255f) },
        { "coronary_artery", new Color(216 / 255f, 101 / 255f, 79 / 255f)}
    };

    public void OnLoadButton()
    {
        UnityEngine.Debug.Log("on load button pressed"); 
        NativeList<JobHandle> jobHandleList = new NativeList<JobHandle>(Allocator.Temp);
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
                    UnityEngine.Debug.Log(error);
                    return; 
                }

                if (!string.IsNullOrEmpty(output))
                {
                    UnityEngine.Debug.Log(output); 
                }
            }

            string[] objFilePathList = Directory.GetFiles(objFolderPath);

            UnityEngine.Debug.Log(objFilePathList.Length);

            foreach (string objFilePath in objFilePathList) 
            {
                string loadedObjectName = Path.GetFileNameWithoutExtension(objFilePath);
                NativeArray<char> objFilePathArray = new NativeArray<char>(objFilePath.ToCharArray(), Allocator.TempJob);

                NativeArray<char> loadedObjectNameArray = new NativeArray<char>(loadedObjectName.ToCharArray(), Allocator.TempJob);

                NativeArray<char> tagArray = new NativeArray<char>(parentObjectTag.ToCharArray(), Allocator.TempJob); 

                LoadFolderJob job = new LoadFolderJob
                {
                    scaleFactor = 0.3f,
                    materialColor = colorDictionary[loadedObjectName],  
                    objFilePathArray = objFilePathArray, 
                    loadedObjectNameArray = loadedObjectNameArray,
                    tagArray = tagArray, 
                };
                jobHandleList.Add(job.Schedule()); 
            }

            JobHandle.CompleteAll(jobHandleList.AsArray());
            jobHandleList.Dispose(); 
        }
    }
}
public struct LoadFolderJob : IJob
{
    public float scaleFactor;
    public Color materialColor;
    public NativeArray<char> objFilePathArray;
    public NativeArray<char> loadedObjectNameArray;
    public NativeArray<char> tagArray; 
    public void Execute()
    { 
        // convert native char array to string
        string objFilePath = new string(objFilePathArray);
        string loadedObjectName = new string(loadedObjectNameArray);
        string tag = new string(tagArray);

        // general config
        GameObject loadedObject = new Dummiesman.OBJLoader().Load(objFilePath);
        GameObject loadedObjectChild = loadedObject.transform.GetChild(0).gameObject;
        UnityEngine.Object.Destroy(loadedObject);
        loadedObjectChild.name = loadedObjectName;
        loadedObjectChild.transform.position = Vector3.zero;
        loadedObjectChild.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);

        // set parent 
        GameObject parentObject = UnityEngine.GameObject.FindWithTag(tag);
        if (parentObject == null) return; 
        loadedObjectChild.transform.SetParent(parentObject.transform, false);

        // set display material
        MeshRenderer childMeshRenderer = loadedObjectChild.GetComponent<MeshRenderer>();
        Material newMaterial = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        newMaterial.color = materialColor; 
        childMeshRenderer.material = newMaterial;

        // set mesh collider
        loadedObjectChild.AddComponent<MeshCollider>();

        // set mesh rigid body 
        loadedObjectChild.AddComponent<Rigidbody>(); 

        // initialize delete slice and destroy slice on input
        DeleteSliceOnButtonPress currentDeleteSliceOnButtonPress = loadedObjectChild.AddComponent<DeleteSliceOnButtonPress>();

        // set delete slice settings
        /*                    currentDeleteSliceOnButtonPress.deleteButton = baseDeleteSliceOnButtonPressScript.deleteButton;*/

        // set enable slice settings
        EnableSlice baseEnableSliceOnButtonPressScript = parentObject.GetComponent<EnableSlice>(); 
        EnableSlice currentEnableSlice = loadedObjectChild.AddComponent<EnableSlice>();
        currentEnableSlice.baseEnableSlice = baseEnableSliceOnButtonPressScript;

        currentEnableSlice.heartTarget = loadedObjectChild;

        currentEnableSlice.crossSectionMaterial = baseEnableSliceOnButtonPressScript.crossSectionMaterial;

        currentEnableSlice.planeObject = baseEnableSliceOnButtonPressScript.planeObject;

    }
}
