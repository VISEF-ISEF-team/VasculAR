using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using TMPro;
using UnityEngine;

public class LoadFolderManagerControllerScript : MonoBehaviour
{
    [SerializeField] Material baseMaterial;
    [SerializeField] GameObject buttonPrefab;
    [SerializeField] GameObject heartSegmentObject;

    // this field is for setting up disappear and appear buttons
    [SerializeField] SegmentCanvas segmentCanvasControllerScript; 

    [SerializeField] GameObject fileContentObject;
    [SerializeField] GameObject folderContentObject;

    // set base enable slice and destroy on button press 
    [SerializeField] EnableSlice baseEnableSlice;
    [SerializeField] DeleteSliceOnButtonPress baseDeleteSliceOnButtonPress;

    // reset button reference
    [SerializeField] ResetPositionButtonActionScript baseResetButtonActionScript; 

    private List<string> folderNameList;
    private string baseDirPath = @"E:\Base_Folder\";

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

            loadFileButtonActionScript.parentObject = heartSegmentObject;
            loadFileButtonActionScript.baseMaterial = baseMaterial;

            // set segment canvas controller script reference
            loadFileButtonActionScript.segmentCanvasControllerScript = segmentCanvasControllerScript;

            // set enable slice and delete slice base scripts
            loadFileButtonActionScript.baseEnableSliceOnButtonPressScript = baseEnableSlice;
            loadFileButtonActionScript.baseDeleteSliceOnButtonPressScript = baseDeleteSliceOnButtonPress;

            // set reset button
            loadFileButtonActionScript.resetButtonActionScript = baseResetButtonActionScript; 

            // set event listener
            loadFileButtonActionScript.SetupOnClickListener();
        }
    }
}
