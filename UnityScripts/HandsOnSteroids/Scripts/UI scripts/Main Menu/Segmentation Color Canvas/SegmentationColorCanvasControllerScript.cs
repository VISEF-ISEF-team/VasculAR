using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class SegmentationColorCanvasControllerScript : MonoBehaviour
{
    public GameObject currentSegment; 
    [SerializeField] Material baseMaterial;
    [SerializeField] MeshRenderer otherSphereRenderer; 

    private GameObject currentTarget; 
    private void Start()
    {
        
    }

    private void Update()
    {
        
    }

    public void SetTarget(GameObject newTarget)
    {
        if (newTarget != null)
        {
            currentTarget = newTarget; 
        }
        SetupButtonForNewSegmentObject(); 
    }

    public void SetupButtonForNewSegmentObject()
    {
        Transform canvasTransform = gameObject.GetComponent<Transform>();
        int currentTargetChildCount = currentTarget.transform.childCount; 
        int counter = 0;
        for (int i = 0; i < canvasTransform.childCount; ++i)
        {
            GameObject childButton = canvasTransform.GetChild(i).gameObject;
            if (childButton == null) continue;
            SegmentColorButtonControllerScript actionScript = childButton.GetComponent<SegmentColorButtonControllerScript>();

            // check if current UI object is button or not
            if (actionScript != null)
            {
                if (counter < currentTargetChildCount)
                {
                    // check if counter is still in child range (which it shoudld) 
                    GameObject currentSegmentInTarget = currentTarget.transform.GetChild(counter).gameObject;

                    // set object for action script
                    actionScript.segmentObject = currentSegmentInTarget; 

                    // set base material
                    actionScript.baseMaterial = baseMaterial;

                    // set other sphere renderer 
                    actionScript.otherSphereRenderer = otherSphereRenderer; 

                    // set name for action script and display 
                    string name = currentSegmentInTarget.name; 
                    actionScript.segmentName = currentSegmentInTarget.name;

                    string[] nameSplit = name.Split("_");
                    if (nameSplit.Length == 1) name = name.ToUpper();
                    else
                    {
                        name = $"{nameSplit[0]} {nameSplit[1]}";
                    }

                    childButton.GetComponentInChildren<TextMeshProUGUI>().text = name;

                    actionScript.SetListener(); 
                    counter++;
                }
                else
                {
                    childButton.GetComponentInChildren<TextMeshProUGUI>().text = "Not assigned";
                    actionScript.segmentName = null;
                }
            }
        }
    }
}
