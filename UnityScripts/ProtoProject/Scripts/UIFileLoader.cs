using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Linq;
using TMPro;

public class UIFileLoader : MonoBehaviour
{
    private List<string> folderNameList;
    private List<string> fileNameList;

    [SerializeField] GameObject buttonPrefab;
    [SerializeField] GameObject fileContentObject;
    [SerializeField] GameObject folderContentObject;
    [SerializeField] GameObject baseObject; 
    
    private string baseDirPath = @"C:\\Users\\Acer\\Downloads\\Base_Folder\\"; 
    private void Start()
    {
        FolderContentSetup();
    }

    private void Update()
    {
        
    }

    private void FolderContentSetup()
    {
        folderNameList = Directory.GetDirectories(baseDirPath).ToList<string>();

        foreach (string folderPath in folderNameList)
        {
            GameObject folderButton = Instantiate(buttonPrefab, Vector3.zero, Quaternion.identity);

            // set text and tweak display 
            TextMeshProUGUI buttonTextMesh = folderButton.GetComponentInChildren<TextMeshProUGUI>();
            buttonTextMesh.text = Path.GetFileName(folderPath);
            folderButton.transform.SetParent(folderContentObject.transform, false);

            // set logic for loading file 
            LoadFileButtonActionScript loadFileButtonActionScript = folderButton.GetComponent<LoadFileButtonActionScript>();
            loadFileButtonActionScript.folderButton = folderButton;
            loadFileButtonActionScript.fileButton = null;

            loadFileButtonActionScript.stlFolderPath = folderPath;
            loadFileButtonActionScript.stlFilePath = null;

            loadFileButtonActionScript.parentObject = baseObject;

            // set event listener
            loadFileButtonActionScript.SetupOnClickListener(); 
        }
    }
}
