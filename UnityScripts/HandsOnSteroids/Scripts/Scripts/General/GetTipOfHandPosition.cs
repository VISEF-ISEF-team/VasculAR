using System.Collections.Generic;
using UnityEngine;

public class GetHandPosition: MonoBehaviour
{
    [SerializeField] GameObject leftHandTip;
    [SerializeField] GameObject rightHandTip;
    public List<Transform> GetHandTipPositions()
    {
        List<Transform> returnList = new()
        {
            leftHandTip.transform,
            rightHandTip.transform
        };
        return returnList; 
    }

    public static GetHandPosition GetHandPositionReference()
    {
        return GameObject.Find("General Settings").GetComponent<GetHandPosition>();
    }
}
