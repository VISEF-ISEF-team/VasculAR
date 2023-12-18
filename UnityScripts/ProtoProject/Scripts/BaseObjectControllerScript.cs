using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; 

public class BaseObjectControllerScript : MonoBehaviour
{
    public List<GameObject> childSegmentObjectList;

    public List<Vector3> oldPosition;

    private void Start()
    {
        oldPosition = new List<Vector3>();
        childSegmentObjectList = new List<GameObject>();
    }
    public void OnResetPositionButtonClick()
    {
        Debug.Log("is called");
        for (int i = 0; i < childSegmentObjectList.Count; i++)
        {
            Debug.Log("inner loop executing");
            childSegmentObjectList[i].transform.position = oldPosition[i]; 
        }
    }

    // relative positioning and snapping into place
    public void SnapBack()
    {
        // Vector3.Distance to calculate the distance to check if the 2 objects are near each other
    }
}