using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ResetPositionButtonActionScript : MonoBehaviour
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
        Debug.Log("reset button is called");
        for (int i = 0; i < childSegmentObjectList.Count; i++)
        {
            childSegmentObjectList[i].transform.position = oldPosition[i];
        }
    }
}
