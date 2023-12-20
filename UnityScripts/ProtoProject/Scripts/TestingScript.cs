using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestingScript : MonoBehaviour
{
    [SerializeField] GameObject planeObject;
    private Vector3 planeExtents; 

    private void Start()
    {
        float xScale = planeObject.transform.localScale.x;
        float zScale = planeObject.transform.localScale.z;
        Vector3 planeObjectPosition = planeObject.transform.position;
        Vector3 planeObjectXDirection = planeObject.transform.right; 
        planeExtents = planeObject.GetComponent<MeshFilter>().mesh.bounds.extents;

        Vector3 deltaPos = planeObjectPosition + (planeObjectXDirection * planeExtents.x * xScale);

        // get new z direction based on object rotation 
        Vector3 newDirection = planeObject.transform.forward;

        // create origin point
        Vector3 origin = planeObject.transform.position + (planeExtents.z * zScale * newDirection);

        origin = origin + (planeObjectXDirection * planeExtents.x * xScale); 
        Debug.Log(origin); 
    }

    private void Update()
    {
        
    }
}

