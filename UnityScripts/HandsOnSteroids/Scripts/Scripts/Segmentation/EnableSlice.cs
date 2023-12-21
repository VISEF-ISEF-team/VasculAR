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

    private Rigidbody heartRigidBody;
    private void Start()
    {
        sliceButton.onClick.AddListener(SliceOnActivate); 
        planeCoordinates = planeObject.transform;
    }

    public void SliceOnActivate() 
    {
        int id = heartTarget.GetInstanceID();
        Debug.Log("instantiate slicing"); 
        Slice(heartTarget, id); 
    }
    public void Slice(GameObject target, int targetInstanceID)
    {
        if (GetIntersection(planeObject, 100.0f, targetInstanceID))
        {
            Debug.Log("get intersecion successful"); 
            SlicedHull hull = target.Slice(planeCoordinates.position, planeCoordinates.up);
            if (hull != null) 
            {
                // upper hull
                GameObject upperHull = hull.CreateUpperHull(target, crossSectionMaterial);
                SliceComponentSetup(upperHull, true, target.name);
                upperHull.transform.position = new Vector3(heartTarget.transform.position.x, heartTarget.transform.position.y + 1.5f, heartTarget.transform.position.z);

                // lower hull
                GameObject lowerHull = hull.CreateLowerHull(target, crossSectionMaterial);
                SliceComponentSetup(lowerHull, false, target.name);
                lowerHull.transform.position = new Vector3(heartTarget.transform.position.x, heartTarget.transform.position.y - 1.5f, heartTarget.transform.position.z);
            }
        }
    }

    public void SliceComponentSetup(GameObject sliceComponent, bool upper, string baseName)
    {
        // set grabbable settings
        XRGrabInteractable currentGrabbable = sliceComponent.AddComponent<XRGrabInteractable>();
        currentGrabbable.useDynamicAttach = true; 

        // set delete on slice
        DeleteSliceOnButtonPress currentDeleteSliceOnButtonPressSettings = sliceComponent.AddComponent<DeleteSliceOnButtonPress>();
        currentDeleteSliceOnButtonPressSettings.deleteButton = baseDeleteSliceOnButtonPress.deleteButton;

        // set enable slice 
        EnableSlice currentEnableSlice = sliceComponent.AddComponent<EnableSlice>();

        currentEnableSlice.heartTarget = sliceComponent; 

        currentEnableSlice.crossSectionMaterial = baseEnableSlice.crossSectionMaterial;

        currentEnableSlice.planeObject = baseEnableSlice.planeObject;   

        currentEnableSlice.baseEnableSlice = baseEnableSlice;

        // set mesh collider
        sliceComponent.AddComponent<MeshCollider>(); 

        // set rigid boy 
        heartRigidBody = sliceComponent.AddComponent<Rigidbody>();
        heartRigidBody.isKinematic = false; 

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

    private bool GetIntersection(GameObject planeObject, float numRay, int targetInstanceID)
    {
        bool res1 = DrawRayXDirection(planeObject, numRay, targetInstanceID);

        bool res2 = DrawRayZDirection(planeObject, numRay, targetInstanceID);

        Debug.Log(res1 && res2);
        return res1 && res2;
    }

    private bool DrawRayXDirection(GameObject planeObject, float numberOfRaysEachSide, int targetInstanceID)
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
                int colliderID = hit.colliderInstanceID;

                // check if collider hit was the inteded target 
                if (!forward && colliderID == targetInstanceID) forward = true;
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
                int colliderID = hit.colliderInstanceID;

                if (!backward && colliderID == targetInstanceID) backward = true;
            }
        }
        return forward && backward;
    }

    private bool DrawRayZDirection(GameObject planeObject, float numberOfRaysEachSide, int targetInstanceID)
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
                int colliderID = hit.colliderInstanceID;
                if (!forward && colliderID == targetInstanceID) forward = true;
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
                int colliderID = hit.colliderInstanceID;
                if (!backward && colliderID == targetInstanceID) backward = true;
            }
        }

        return forward && backward;
    }
}
