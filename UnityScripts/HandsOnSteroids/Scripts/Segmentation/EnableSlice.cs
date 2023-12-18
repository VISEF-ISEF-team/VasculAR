using UnityEngine;
using EzySlice;
using UnityEngine.XR.Interaction.Toolkit;

public class EnableSlice : MonoBehaviour
{
    private XRGrabInteractable grabbable;
    public EnableSlice baseEnableSlice; 
    public GameObject heartTarget;
    public Material crossSectionMaterial;
    public GameObject planeObject;
    public DeleteSliceOnButtonPress baseDeleteSliceOnButtonPress;

    private readonly string layerName = "Interactable"; 
    private Transform planeCoordinates; 

    private Rigidbody heartRigidBody;

    private void Start()
    {
        grabbable = GetComponent<XRGrabInteractable>();
        grabbable.activated.AddListener(SliceOnActivate);
        planeCoordinates = planeObject.transform;
    }

    private void SliceOnActivate(ActivateEventArgs activateEventArgs) 
    {
        int id = heartTarget.GetInstanceID();
        Slice(heartTarget, id); 
    }
    public void Slice(GameObject target, int targetInstanceID)
    {
        if (GetIntersection(planeObject, 100.0f, targetInstanceID))
        {
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
        XRGrabInteractable sliceGrabbable = sliceComponent.AddComponent<XRGrabInteractable>();

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

            // positive X
            float newX = planeObject.transform.position.x + (planeExtents.x * xScale);
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z + (planeExtents.z * zScale) - zStep * i;

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(-1, 0, 0), out RaycastHit hit, zMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                int colliderID = hit.colliderInstanceID;

                // check if collider hit was the inteded target 
                if (!forward && colliderID == targetInstanceID) forward = true;
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

        for (int i = 0; i < numberOfRaysEachSide; i++)
        {
            float newX = planeObject.transform.position.x + (planeExtents.x * xScale) - xStep * i;
            float newY = planeObject.transform.position.y;
            float newZ = planeObject.transform.position.z + (planeExtents.z * zScale);

            Vector3 origin = new Vector3(newX, newY, newZ);

            if (Physics.Raycast(origin, new Vector3(0, 0, -1), out RaycastHit hit, xMaxDistance))
            {
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                int colliderID = hit.colliderInstanceID;
                if (!forward && colliderID == targetInstanceID) forward = true;
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
                Debug.DrawLine(origin, hit.point, Color.green, 100.0f);
                int colliderID = hit.colliderInstanceID;
                if (!backward && colliderID == targetInstanceID) backward = true;
            }
        }

        return forward && backward;
    }
}
