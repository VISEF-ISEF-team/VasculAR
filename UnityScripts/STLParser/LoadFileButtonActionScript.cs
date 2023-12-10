using UnityEditor;
using UnityEngine;
using System.IO;

public class LoadFileButtonActionScript : MonoBehaviour
{
    public string objFilePath; // Assign the path to the OBJ file in the Inspector
    public void LoadFile()
    {
        string filePath = UnityEditor.EditorUtility.OpenFilePanel("Select Image", "", "png,jpg,jpeg");
        if (!string.IsNullOrEmpty(filePath))
        {
        }
}
