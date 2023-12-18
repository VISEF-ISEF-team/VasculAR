using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class SegmentCanvas : MonoBehaviour
{
    public GameObject segmentObject;
    [SerializeField] GameObject segmentCanvas;

    private float maxScale = 3.0f;
    private float minScale = 0.5f;

    private List<string> segmentNameList; 

    public void StartSetupProcess()
    {
        segmentNameList = new List<string>();

        for (int i = 0; i < segmentObject.transform.childCount; ++i)
        {
            GameObject child = segmentObject.transform.GetChild(i).gameObject;
            segmentNameList.Add(child.name); 
        }
        SetupButton();
    }
    private void SetupButton()
    {
        Transform canvasTransform = segmentCanvas.GetComponent<Transform>();
        int counter = 0; 
        for (int i = 0; i < canvasTransform.childCount; ++i)
        {
            GameObject child = canvasTransform.GetChild(i).gameObject;
            SegmentButtonActionScript actionScript = child.GetComponent<SegmentButtonActionScript>(); 
            if (actionScript != null)
            {
                if (counter < segmentNameList.Count)
                {
                    string name = segmentNameList[counter];
                    actionScript.segmentName = name;

                    string[] nameSplit = name.Split("_");
                    if (nameSplit.Length == 1) name = name.ToUpper(); 
                    else
                    {
                        name = $"{nameSplit[0]} {nameSplit[1]}"; 
                    }

                    child.GetComponentInChildren<TextMeshProUGUI>().text = name; 
                    counter++;

                    actionScript.segmentObjectChild = segmentObject.transform.Find(segmentNameList[counter]).gameObject;
                }
                else
                {
                    child.GetComponentInChildren<TextMeshProUGUI>().text = "Not assigned";
                    actionScript.segmentName = null;
                }
            }
        }
    }

    public void OnSliderChangeSphereSize(float scale)
    {
        scale = Mathf.Clamp(scale, maxScale, minScale);
        segmentObject.transform.localScale = new Vector3(scale, scale, scale);
    }
}
