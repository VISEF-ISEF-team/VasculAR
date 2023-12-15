using Dummiesman;
using System.IO;
using UnityEngine;

public class ObjFromFile : MonoBehaviour
{
    [SerializeField] Material newMaterial; 
    private MeshRenderer childMeshRenderer; 
    string objPath = string.Empty;
    string error = string.Empty;
    GameObject loadedObject;

    void OnGUI() {
        objPath = GUI.TextField(new Rect(0, 0, 256, 32), objPath);

        GUI.Label(new Rect(0, 0, 256, 32), "Obj Path:");
        if(GUI.Button(new Rect(256, 32, 64, 32), "Load File"))
        {
            //file path
            if (!File.Exists(objPath))
            {
                error = "File doesn't exist.";
            }
            else
            {
                if (loadedObject != null) Destroy(loadedObject);
                loadedObject = new OBJLoader().Load(objPath);
                error = string.Empty;
                loadedObject.name = "changed";
                loadedObject.transform.position = Vector3.zero;
                loadedObject.transform.localScale = new Vector3(0.005f, 0.005f, 0.005f);
                childMeshRenderer = loadedObject.GetComponentInChildren<MeshRenderer>();
                childMeshRenderer.material = newMaterial; 
            }
        }


        if (!string.IsNullOrWhiteSpace(error))
        {
            GUI.color = Color.red;
            GUI.Box(new Rect(0, 64, 256 + 64, 32), error);
            GUI.color = Color.white;
        }
    }
}
