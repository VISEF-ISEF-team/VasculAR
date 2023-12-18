using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestingScript : MonoBehaviour
{
    [SerializeField] GameObject planeObject; 
    [SerializeField] bool show = false;
    [SerializeField] GameObject cubeObject;
    [SerializeField] float numRay; 
    private MeshRenderer planeMeshRenderer;

    private MeshFilter planeMeshFilter; 
    private Mesh planeMesh; 
    // get the bounds of the slicer object
    // then calculate whether points of the object that will be sliced if slicer object is intersecting it
    private void Start()
    {
        planeMeshRenderer = planeObject.GetComponent<MeshRenderer>();
        planeMeshFilter = planeObject.GetComponent<MeshFilter>();
        planeMesh = planeMeshFilter.mesh; 
    }
    private void Update()
    {
        // cast a ray from center of cube, with y level modified to the y level of plane, to the four faces of the cube. 
        // if the ray hits plane, cube, plane => intersecting
        // if the ray hits cube only => not intersecting
        // if the ray hits plane then cube only => not intersecting
        // only if ray hits 4 direction in order of plane cube plane does it intersect

        if (show)
        {
            Debug.Log(GetIntersection(planeObject, numRay));
            show = false; 
        }
    }

    private bool GetIntersection(GameObject planeObject, float numRay)
    {
        return DrawRayXDirection(planeObject, numRay) && DrawRayZDirection(planeObject, numRay); 
    }

    private bool DrawRayXDirection(GameObject planeObject, float numberOfRaysEachSide)
    {
        bool forward = false;
        bool backward = false; 
        Bounds planeMeshBound = planeObject.GetComponent<MeshFilter>().mesh.bounds; 
        Vector3 planeExtents = planeMeshBound.extents;

        float xScale = planeObject.transform.localScale.x;
        float zScale = planeObject.transform.localScale.z;

        float zMaxDistance = planeExtents.z * 2 * zScale;
        float zStep = zMaxDistance / numberOfRaysEachSide;

        float maxZ = planeObject.transform.position.z + (planeExtents.z * zScale);
        float minZ = planeObject.transform.position.z - (planeExtents.z * zScale);

        // positive X direction ray cast, ray then move in Z direction 
        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            // center.x + extents.x, center.y, center.z + extents.z 
            // then we change what we add to the center.z to move it down
            // each step will be extents.z * 2 * scale / step 

            // positive X
            float newX = planeObject.transform.position.x + (planeExtents.x * xScale);
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z + (planeExtents.z * zScale) - zStep * i;

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(-1, 0, 0), out RaycastHit hit, zMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                if (!forward) forward = true; 
            }
            else
            {
                Debug.DrawLine(origin, new Vector3(planeObject.transform.position.x - (planeExtents.x * xScale), origin.y, origin.z), Color.red, 100.0f);
            }
        }

        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            // center.x + extents.x, center.y, center.z + extents.z 
            // then we change what we add to the center.z to move it down
            // each step will be extents.z * 2 * scale / step 

            // positive X
            float newX = planeObject.transform.position.x - (planeExtents.x * xScale);
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z + (planeExtents.z * zScale) - zStep * i;

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(1, 0, 0), out RaycastHit hit, zMaxDistance))
            {
                if (!backward) backward = true;
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
            }
        }
        return forward && backward; 
    }

    private bool DrawRayZDirection(GameObject planeObject, float numberOfRaysEachSide)
    {
        bool forward = false;
        bool backward = false; 

        Bounds planeMeshBound = planeObject.GetComponent<MeshFilter>().mesh.bounds;
        Vector3 planeExtents = planeMeshBound.extents;

        float xScale = planeObject.transform.localScale.x;
        float zScale = planeObject.transform.localScale.z; 

        float xMaxDistance = planeExtents.x * 2 * xScale;
        float xStep = xMaxDistance / numberOfRaysEachSide;

        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            float newX = planeObject.transform.position.x + (planeExtents.x * xScale) - xStep * i;
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z + (planeExtents.z * zScale);

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(0, 0, -1), out RaycastHit hit, xMaxDistance))
            {
                if (!forward) forward = true; 
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
            }
            else
            {
                Debug.DrawLine(origin, new Vector3(origin.x, origin.y, planeObject.transform.position.z - (planeExtents.z * zScale)), Color.red, 100.0f);
            }
        }

        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            float newX = planeObject.transform.position.x + (planeExtents.x * xScale) - xStep * i;
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z - (planeExtents.z * zScale);

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(0, 0, 1), out RaycastHit hit, xMaxDistance))
            {
                if (!backward) backward = true; 
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
            }
        }

        return forward && backward; 
    }
    
    // implement full intersection
}

