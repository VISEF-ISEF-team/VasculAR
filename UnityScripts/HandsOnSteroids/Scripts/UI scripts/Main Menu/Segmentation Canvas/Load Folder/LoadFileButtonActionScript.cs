using UnityEditor;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using Dummiesman;
using System.IO;
using UnityEngine.XR.Interaction.Toolkit;
using System.Collections.Generic;
using UnityEngine.UI; 

#nullable enable
public class LoadFileButtonActionScript : MonoBehaviour
{
    // have another script control all of the buttons in the folder 

    // base material is assigned as asset 
    public Material baseMaterial; 

    // parentObject is the heart segment object in Unity, which is an empty object with scripts only 
    public GameObject parentObject;

    // this field is for setting up disappear and appear buttons
    public SegmentCanvas segmentCanvasControllerScript;

    // files for clicking logic and loading files 
    public GameObject? folderButton;
    public GameObject? fileButton;
    public string stlFolderPath;
    public string stlFilePath;

    // base configs on heart segment object 
    public DeleteSliceOnButtonPress baseDeleteSliceOnButtonPressScript;
    public EnableSlice baseEnableSliceOnButtonPressScript;

    // color coding 
    private Color singleColor = new Color(22 / 255f, 48 / 255f, 32 / 255f);
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

    // reset position button 
    public ResetPositionButtonActionScript resetButtonActionScript; 

    // error logic
    private bool folderCoroutineError = false;
    private bool fileCorountineError = false;
    private float scaleFactor = 0.007f;

    // name for layer 
    private readonly string layerName = "Interactable";

    private void Start()
    {
        baseDeleteSliceOnButtonPressScript = parentObject.GetComponent<DeleteSliceOnButtonPress>();
        baseEnableSliceOnButtonPressScript = parentObject.GetComponent<EnableSlice>(); 
    }
    private void Update()
    {
        if (folderCoroutineError)
        {
            StopCoroutine(LoadFileCoroutine(stlFolderPath));
            folderCoroutineError = false;
        }

        if (fileCorountineError)
        {
            StopCoroutine(LoadFileCoroutine(stlFilePath));
            fileCorountineError = false;
        }
    }

    public void LoadFolder()
    {
        UnityEngine.Debug.Log("Load Folder");
        if (!string.IsNullOrEmpty(stlFolderPath))
        {
            StartCoroutine(LoadFolderCoroutine(stlFolderPath));
        }
    }

    public void LoadFile()
    {
        if (!string.IsNullOrEmpty(stlFilePath))
        {
            StartCoroutine(LoadFileCoroutine(stlFilePath));
        }
    }

    private IEnumerator LoadFileCoroutine(string stlFilePath)
    {
        string interpreterPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\.venv\\Scripts\\python.exe";
        string parserFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\parse.py";
        string objFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\output_file.obj";

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
                    fileCorountineError = true;
                    StopCoroutine(LoadFileCoroutine(stlFilePath));
                }
                else if (!string.IsNullOrEmpty(output))
                {
                    UnityEngine.Debug.Log(output);
                    fileCorountineError = true;
                }

                if (HasChildren(parentObject.transform))
                {
                    DeleteChildren(parentObject.transform);
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

                GameObject loadedObject = new OBJLoader().Load(objFilePath);
                loadedObject.name = loadedObjectName;
                loadedObject.transform.position = Vector3.zero;
                loadedObject.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);
                MeshRenderer childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>();
                childMeshRenderer.material.color = singleColor;
            }
        }
        else
        {
            fileCorountineError = true;
            yield return null;
        }
    }

    private IEnumerator LoadFolderCoroutine(string stlFolderPath)
    {
        string interpreterPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\.venv\\Scripts\\python.exe";
        string parserFilePath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\parse.py";
        string objFolderPath = @"E:\\ISEF\\VasculAR2\\VascuIAR\\UnityScripts\\STLParser\\\obj_folder\\";

        UnityEngine.Debug.Log("load folder coroutine"); 

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
                    folderCoroutineError = true;
                    StopCoroutine(LoadFileCoroutine(stlFolderPath));
                }
                else if (!string.IsNullOrEmpty(output))
                {
                    UnityEngine.Debug.Log(output);
                    folderCoroutineError = true;
                }

                if (HasChildren(parentObject.transform))
                {
                    DeleteChildren(parentObject.transform);
                }

                string[] objFileList = Directory.GetFiles(objFolderPath);

                // loop through all the file in Object Folder
                foreach (string filePath in objFileList)
                {
                    // initialize object to spawn 
                    string loadedObjectName = Path.GetFileNameWithoutExtension(filePath);
                    GameObject loadedObject = new OBJLoader().Load(filePath);

                    // general config
                    GameObject loadedObjectChild = loadedObject.transform.GetChild(0).gameObject;
                    Destroy(loadedObject); 
                    loadedObjectChild.name = loadedObjectName;
                    loadedObjectChild.transform.position = Vector3.zero;
                    loadedObjectChild.transform.localScale = new Vector3(scaleFactor, scaleFactor, scaleFactor);

                    // set child object (which name is the name of the heart segment)
                    if (HasChildren(parentObject.transform))
                    {
                        GameObject newParentObject = new GameObject();
                        newParentObject.transform.position = parentObject.transform.position + new Vector3(0.5f, 0, 0);
                        parentObject = newParentObject; 
                    }
                    loadedObjectChild.transform.SetParent(parentObject.transform, false);

                    // set layer for object 
                    loadedObjectChild.layer = LayerMask.NameToLayer(layerName);

                    // set display material 
                    MeshRenderer childMeshRenderer = loadedObjectChild.GetComponent<MeshRenderer>();
                    Material newMaterial = Instantiate(baseMaterial);
                    newMaterial.color = colorDictionary[loadedObjectChild.name];
                    UnityEngine.Debug.Log(colorDictionary[loadedObject.name]);
                    childMeshRenderer.material = newMaterial;

                    // try to optimize mesh for slicing 
                    Mesh childMesh = loadedObjectChild.GetComponent<MeshFilter>().mesh;
                    childMesh.Optimize(); 
                    
                    // add rigid body 
                    Rigidbody currentRigidBody = loadedObjectChild.AddComponent<Rigidbody>();
                    currentRigidBody.isKinematic = true; 
                    currentRigidBody.useGravity = false;

                    // add mesh collider
                    loadedObjectChild.AddComponent<MeshCollider>();

                    // add grab interactable
                    XRGrabInteractable currentGrabbable =  loadedObjectChild.AddComponent<XRGrabInteractable>();
                    currentGrabbable.useDynamicAttach = true; 

                    // initialize delete slice and destroy slice on input
                    DeleteSliceOnButtonPress currentDeleteSliceOnButtonPress = loadedObjectChild.AddComponent<DeleteSliceOnButtonPress>();   
                    EnableSlice currentEnableSlice = loadedObjectChild.AddComponent<EnableSlice>();

                    // set delete slice settings
                    currentDeleteSliceOnButtonPress.deleteButton = baseDeleteSliceOnButtonPressScript.deleteButton;

                    // set enablie slice settings
                    currentEnableSlice.baseEnableSlice = baseEnableSliceOnButtonPressScript; 
                    currentEnableSlice.heartTarget = loadedObjectChild; 
                    currentEnableSlice.crossSectionMaterial = baseEnableSliceOnButtonPressScript.crossSectionMaterial;
                    currentEnableSlice.planeObject = baseEnableSliceOnButtonPressScript.planeObject;
                    currentEnableSlice.sliceButton = baseEnableSliceOnButtonPressScript.sliceButton;
                    currentEnableSlice.baseDeleteSliceOnButtonPress = baseDeleteSliceOnButtonPressScript; 

                    // set position for reset button 
                    resetButtonActionScript.childSegmentObjectList.Add(loadedObjectChild);
                    resetButtonActionScript.oldPosition.Add(loadedObjectChild.transform.position); 

                }
                // set hide and show button on canvas
                segmentCanvasControllerScript.StartSetupProcess();
                segmentCanvasControllerScript.AddSegmentObjectToList(parentObject, stlFolderPath); 
            }
            yield return null;
        }
        else
        {
            folderCoroutineError = true;
            yield return null;
        }
        yield return null;
    }

    public void SetupOnClickListener()
    {
        if (folderButton != null)
        {
            UnityEngine.Debug.Log("folderButton is not null");
            folderButton.GetComponent<Button>().onClick.AddListener(LoadFolder);
        }
        else if (fileButton != null)
        {
            fileButton.GetComponent<Button>().onClick.AddListener(LoadFile);
        }
    }

    private void DeleteChildren(Transform parent)
    {
        // Loop through each child of the parent
        for (int i = parent.childCount - 1; i >= 0; i--)
        {
            // Destroy the child GameObject
            Destroy(parent.GetChild(i).gameObject);
        }
    }

    private bool HasChildren(Transform parent)
    {
        // Check if the parent has any children
        return parent.childCount > 0;
    }
}

