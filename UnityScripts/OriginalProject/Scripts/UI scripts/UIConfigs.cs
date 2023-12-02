using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UIConfigs : MonoBehaviour
{
    public float spawnDistance = 2.0f;
    public Transform headConfigObjectTransform; 

    public Vector3 TransformPositionInFrontOfHead(Transform head, float spawnDistance)
    {
        return head.position + new Vector3(head.forward.x, 0, head.forward.z).normalized * spawnDistance;
    }
}
