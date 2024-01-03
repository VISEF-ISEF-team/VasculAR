using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.InputSystem;

public class MeasureObjectActionScript : MonoBehaviour
{
    [SerializeField] GameObject startingMeasurePoint;
    [SerializeField] GameObject endingMeasurepoint;
    [SerializeField] InputActionProperty rightTriggerButton;
    [SerializeField] InputActionProperty leftTriggerButton;

    private GetHandPosition handPositions;
    private readonly float xoffset = 0.05f;
    private bool allowLeftHand;
    public bool AllowLeftHand
    {
        get { return allowLeftHand; }
        set { if (allowLeftHand != value) allowLeftHand = value; }
    }
    private Vector3 measurePointScale;
    public Vector3 MeasurePointScale
    {
        get { return measurePointScale; }
        set { measurePointScale = value;  }
    }
    private bool isStarting = true;
    private GameObject currentActiveSphere;
    private GameObject currentActiveOtherSphere;

    private List<GameObject> measurePointList = new List<GameObject>();
    public List<GameObject> MeasurePointList
    { get { return measurePointList; } }

    private static int currentColorIndex = 0; 
    private List<Color> colorList = new List<Color>()
    {
        // write in color codes for measure points
        new Color(1.0f, 0.0f, 0.0f, 1.0f),
        new Color(0.0f, 1.0f, 0.0f, 1.0f), 
        new Color(0.0f, 0.0f, 1.0f, 1.0f), 
        new Color(1.0f, 1.0f, 0.0f, 1.0f), 
        new Color(1.0f, 0.0f, 1.0f, 1.0f), 
        new Color(0.0f, 1.0f, 1.0f, 1.0f), 
        new Color(1.0f, 1.0f, 1.0f, 1.0f), 
        new Color(0.5f, 0.5f, 0.5f, 1.0f), 
        new Color(0.0f, 0.0f, 0.0f, 1.0f), 
        new Color(0.6f, 0.8f, 1.0f, 1.0f), 
        new Color(0.7f, 1.0f, 0.7f, 1.0f), 
        new Color(1.0f, 0.7f, 0.7f, 1.0f), 
        new Color(1.0f, 0.5f, 0.0f, 1.0f), 
        new Color(0.5f, 0.0f, 1.0f, 1.0f), 
        new Color(0.0f, 0.5f, 0.5f, 1.0f)
    };
    private void Start()
    {
        handPositions = GetHandPosition.GetHandPositionReference();
    }

    private void Update()
    {
        // only for when the sphere is immediately initialized 
        Transform rightHandTip = handPositions.GetHandTipPositions()[1];
        Vector3 rightHandTipPosition = new Vector3(rightHandTip.position.x + xoffset, rightHandTip.position.y, rightHandTip.position.z);

        if (allowLeftHand)
        {
            Transform leftHandTip = handPositions.GetHandTipPositions()[0];
            Vector3 leftHandTipPosition = new Vector3(leftHandTip.position.x + xoffset, leftHandTip.position.y, leftHandTip.position.z);
            if (isStarting)
            {
                if (leftTriggerButton.action.WasPressedThisFrame())
                {
                    Color sphereColor = GetColor();
                    GameObject startSphere = Instantiate(startingMeasurePoint, leftHandTipPosition, Quaternion.identity);
                    startSphere.transform.localScale = measurePointScale;
                    startSphere.GetComponentInChildren<MeshRenderer>().material.color = sphereColor;

                    GameObject endSphere = Instantiate(endingMeasurepoint, leftHandTipPosition, Quaternion.identity);
                    endSphere.transform.localScale = measurePointScale;
                    endSphere.GetComponentInChildren<MeshRenderer>().material.color = sphereColor;

                    MeasurePointActionScript measurePointScript = startSphere.GetComponent<MeasurePointActionScript>();
                    measurePointScript.endSphere = endSphere;
                    measurePointScript.InitializeStartingSphere();
                    isStarting = false;
                    measurePointList.Add(startSphere);
                    currentActiveSphere = startSphere;
                    currentActiveOtherSphere = endSphere;
                }
            }
            else
            {
                currentActiveSphere.GetComponent<MeasurePointActionScript>().SetLineRendererPosition(1, leftHandTipPosition);
                currentActiveOtherSphere.transform.position = leftHandTipPosition;
                currentActiveOtherSphere.GetComponent<MeasurePointActionScript>().SetDistanceText();
                if (leftTriggerButton.action.WasPressedThisFrame())
                {
                    isStarting = true;
                }
            }
        }
        else
        {
            if (isStarting)
            {
                if (rightTriggerButton.action.WasPressedThisFrame())
                {
                    Color sphereColor = GetColor();
                    GameObject startSphere = Instantiate(startingMeasurePoint, rightHandTipPosition, Quaternion.identity);
                    startSphere.SetActive(true); 
                    // set start sphere color 
                    startSphere.GetComponentInChildren<MeshRenderer>().material.color = sphereColor;
                    startSphere.transform.localScale = measurePointScale;

                    GameObject endSphere = Instantiate(endingMeasurepoint, rightHandTipPosition, Quaternion.identity);
                    endSphere.SetActive(true);
                    endSphere.GetComponentInChildren<MeshRenderer>().material.color = sphereColor;
                    endSphere.transform.localScale = measurePointScale;

                    // attach end sphere to start sphere
                    MeasurePointActionScript measurePointScript = startSphere.GetComponent<MeasurePointActionScript>();
                    measurePointScript.endSphere = endSphere;
                    measurePointScript.InitializeStartingSphere();
                    measurePointList.Add(startSphere);
                    currentActiveSphere = startSphere;
                    currentActiveOtherSphere = endSphere;
                    isStarting = false;
                }
            }
            else
            {
                currentActiveSphere.GetComponent<MeasurePointActionScript>().SetLineRendererPosition(1, rightHandTipPosition);
                currentActiveOtherSphere.transform.position = rightHandTipPosition;
                currentActiveOtherSphere.GetComponent<MeasurePointActionScript>().SetDistanceText();
                if (rightTriggerButton.action.WasPressedThisFrame())
                {
                    isStarting = true;
                }
            }
        }
    }

    Color GetColor()
    {
        if (currentColorIndex >= colorList.Count() - 1)
        {
            currentColorIndex = 0;
        }
        Color currentColor = colorList[currentColorIndex]; 
        if (currentColor != null) 
        {
            currentColorIndex++;
        }
        return currentColor; 
    }

    public void SetDeleteStatusForMeasurePoints()
    {
        foreach (var points in measurePointList)
        {
            MeasurePointActionScript pointActionScript = points.GetComponent<MeasurePointActionScript>();
            pointActionScript.AllowDelete = !pointActionScript.AllowDelete;
        }
    }

    public void SetGrabStatusForMeasurePoints(bool value)
    {
        foreach (var points in measurePointList) 
        {
            MeasurePointActionScript pointActionScript= points.GetComponent<MeasurePointActionScript>();
            pointActionScript.AllowGrab = value; 
        }
    }
}
