using UnityEngine;
using Dummiesman;
using System.IO; 

public class MeshReconstruct : MonoBehaviour
{
    [SerializeField] Material newMaterial; 
    private GameObject loadedObject; 
    private void Start()
    {
        string obj_file_path = "E:\\ISEF\\VascuIAR\\UnityScripts\\STLParser\\output_file.obj";
        loadedObject = new OBJLoader().Load(obj_file_path);
        loadedObject.transform.position = Vector3.zero;
        loadedObject.transform.localScale = new Vector3(0.007f, 0.007f, 0.007f);
        MeshRenderer childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>();
        childMeshRenderer.material = newMaterial;
    }

    private void Update()
    {
        
    }
}
