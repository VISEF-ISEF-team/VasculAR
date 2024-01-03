using UnityEngine;
using EzySlice;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.UI;

public class EnableSlice : MonoBehaviour
{
    public EnableSlice baseEnableSlice; 
    public GameObject heartTarget;
    public Material crossSectionMaterial;
    public GameObject planeObject;
    public DeleteSliceOnButtonPress baseDeleteSliceOnButtonPress;
    public Button sliceButton;

    private readonly string layerName = "Interactable"; 
    private Transform planeCoordinates;

    private float spawnPostionOffset = 0.5f; 
    private Rigidbody heartRigidBody;
    private void Start()
    {
        sliceButton.onClick.AddListener(SliceOnActivate); 
        planeCoordinates = planeObject.transform;
    }

    public void SliceOnActivate() 
    {
        Slice(heartTarget); 
    }
    public void Slice(GameObject target)
    {
        Debug.Log($"Target: {target}"); 
        if (GetIntersection(planeObject, 100.0f))
        {
            Debug.Log("get intersecion successful"); 
            SlicedHull hull = target.Slice(planeCoordinates.position, planeCoordinates.up);
            if (hull != null) 
            {
                // create transform direction 
                Vector3 transformOffsetDirection = planeObject.transform.up; 

                // upper hull
                GameObject upperHull = hull.CreateUpperHull(target, crossSectionMaterial);
                SliceComponentSetup(upperHull, true, target.name);
                upperHull.transform.position = heartTarget.transform.position + transformOffsetDirection * spawnPostionOffset; 

                // lower hull
                GameObject lowerHull = hull.CreateLowerHull(target, crossSectionMaterial);
                SliceComponentSetup(lowerHull, false, target.name);
                lowerHull.transform.position = heartTarget.transform.position + transformOffsetDirection * -1 * spawnPostionOffset;
            }
        }
    }

    public void SliceComponentSetup(GameObject sliceComponent, bool upper, string baseName)
    {
        sliceComponent.transform.localScale = sliceComponent.transform.localScale * (float) 0.3; 

        // set delete on slice
        DeleteSliceOnButtonPress currentDeleteSliceOnButtonPressSettings = sliceComponent.AddComponent<DeleteSliceOnButtonPress>();
        currentDeleteSliceOnButtonPressSettings.deleteButton = baseDeleteSliceOnButtonPress.deleteButton;

        // set enable slice 
        EnableSlice currentEnableSlice = sliceComponent.AddComponent<EnableSlice>();

        currentEnableSlice.heartTarget = sliceComponent; 

        currentEnableSlice.crossSectionMaterial = baseEnableSlice.crossSectionMaterial;

        currentEnableSlice.planeObject = baseEnableSlice.planeObject;   

        currentEnableSlice.baseEnableSlice = baseEnableSlice;

        currentEnableSlice.sliceButton = baseEnableSlice.sliceButton;

        // set mesh collider
        sliceComponent.AddComponent<MeshCollider>(); 

        // set rigid boy 
        heartRigidBody = sliceComponent.AddComponent<Rigidbody>();
        heartRigidBody.isKinematic = true; 

        // set grabbable settings
        XRGrabInteractable currentGrabbable = sliceComponent.AddComponent<XRGrabInteractable>();
        currentGrabbable.useDynamicAttach = true; 

        // set layer for slice component
        sliceComponent.layer = LayerMask.NameToLayer(layerName); 

        // set name for sliced component
        if (upper)
        {
            sliceComponent.name = $"{baseName}-upper";
        }
        else
        {
            sliceComponent.name = $"{baseName}-lower"; 
        }
    }

    private bool GetIntersection(GameObject planeObject, float numRay)
    {
        bool res1 = DrawRayXDirection(planeObject, numRay);

        bool res2 = DrawRayZDirection(planeObject, numRay);

        Debug.Log(res1);
        Debug.Log(res2); 
        return res1 && res2;
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

        // positive X direction ray cast, ray then move in Z direction 
        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            // center.x + extents.x, center.y, center.z + extents.z 
            // then we change what we add to the center.z to move it down
            // each step will be extents.z * 2 * scale / step 

            // center.x + extents.x, center.y, center.z + extents.z 
            // then we change what we add to the center.z to move it down
            // each step will be extents.z * 2 * scale / step 

            // positive x

            // get new direction that is already calculated based on object's rotation 
            Vector3 xDirection = planeObject.transform.right;
            Vector3 zDirection = planeObject.transform.forward;

            // calculate new starting point base on new direction vector
            Vector3 origin = planeObject.transform.position + (planeExtents.x * xScale * xDirection);
            origin = origin + (zDirection * planeExtents.z * zScale) - zDirection * zStep * i;

            // calculate new ray end point 
            Vector3 endPoint = planeObject.transform.position + (planeExtents.x * xScale * -xDirection);
            endPoint = endPoint + (zDirection * planeExtents.z * zScale) - zDirection * zStep * i;

            if (Physics.Raycast(origin, -xDirection, out RaycastHit hit, zMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);

                // check if collider hit was the inteded target 
                if (!forward && hit.collider.gameObject == heartTarget)
                {
                    forward = true;
                    Debug.Log(hit.collider.gameObject); 
                }
            }
            else
            {
                Debug.DrawLine(origin, endPoint, Color.red, 100.0f);
            }
        }

        // negative X 
        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            Vector3 xDirection = -planeObject.transform.right;
            Vector3 zDirection = planeObject.transform.forward;

            Vector3 origin = planeObject.transform.position + (planeExtents.x * xScale * xDirection);
            origin = origin + (zDirection * planeExtents.z * zScale) - zDirection * zStep * i;

            if (Physics.Raycast(origin, -xDirection, out RaycastHit hit, zMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                if (!backward && hit.collider.gameObject == heartTarget)
                {
                    backward = true;
                    Debug.Log(hit.collider.gameObject); 
                }
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

        // positive z direction 
        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            // get new z direction based on object rotation 
            Vector3 zDirection = planeObject.transform.forward;
            Vector3 xDirection = planeObject.transform.right;

            // create origin point
            Vector3 origin = planeObject.transform.position + (planeExtents.z * zScale * zDirection);
            origin = origin + (xDirection * planeExtents.x * xScale) - xDirection * xStep * i;

            // create endpoint 
            Vector3 endPoint = planeObject.transform.position + (planeExtents.z * zScale * -zDirection);
            endPoint = endPoint + (xDirection * planeExtents.x * xScale) - xDirection * xStep * i;

            if (Physics.Raycast(origin, -zDirection, out RaycastHit hit, xMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                if (!forward && hit.collider.gameObject == heartTarget) forward = true;
            }
            else
            {
                Debug.DrawLine(origin, endPoint, Color.red, 100.0f);
            }
        }

        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            // get new z direction based on object rotation 
            Vector3 zDirection = -planeObject.transform.forward;
            Vector3 xDirection = planeObject.transform.right;

            // create origin point
            Vector3 origin = planeObject.transform.position + (planeExtents.z * zScale * zDirection);
            origin = origin + (xDirection * planeExtents.x * xScale) - xDirection * xStep * i;

            if (Physics.Raycast(origin, -zDirection, out RaycastHit hit, xMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                if (!backward && hit.collider.gameObject == heartTarget) backward = true;
            }
        }

        return forward && backward;
    }
}
