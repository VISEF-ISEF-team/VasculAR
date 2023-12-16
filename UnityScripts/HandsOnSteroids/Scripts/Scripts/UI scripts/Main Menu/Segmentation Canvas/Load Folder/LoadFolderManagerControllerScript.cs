using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using TMPro;
using UnityEngine;

public class LoadFolderManagerControllerScript : MonoBehaviour
{
    [SerializeField] Material baseMaterial;
    [SerializeField] GameObject baseObject;
    [SerializeField] GameObject buttonPrefab;
    [SerializeField] GameObject heartSegmentObject; 

    [SerializeField] GameObject fileContentObject;
    [SerializeField] GameObject folderContentObject;

    private EnableSlice enableSliceScript;
    private DeleteSliceOnButtonPress deleteSliceOnButtonPressScript; 

    private List<string> folderNameList;
    private string baseDirPath = @"C:\\Users\\Acer\\Downloads\\Base_Folder\\";
    private void Start()
    {
        enableSliceScript = heartSegmentObject.GetComponent<EnableSlice>();
        deleteSliceOnButtonPressScript = heartSegmentObject.GetComponent<DeleteSliceOnButtonPress>();   
    }

    private void OnEnable()
    {
        FolderContentSetup(); 
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
            loadFileButtonActionScript.baseMaterial = baseMaterial;

            // set event listener
            loadFileButtonActionScript.SetupOnClickListener();
        }
    }
}
