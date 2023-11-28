using System.Collections.Generic;
using UnityEngine;

public class GetHandPosition: ScriptableObject
{
    private Transform leftHandTip;
    private Transform rightHandTip;
    public void StartScript()
    {
        leftHandTip = GameObject.Find("RightGrabRay").transform;
        rightHandTip = GameObject.Find("LeftGrabRay").transform; 
    }
    public List<Transform> GetHandTipPositions()
    {
        List<Transform> returnList = new()
        {
            leftHandTip,
            rightHandTip
        };
        return returnList; 
    }
}
