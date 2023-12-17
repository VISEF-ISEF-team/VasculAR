using UnityEngine;
using EzySlice;
using UnityEngine.XR.Interaction.Toolkit;

public class EnableSlice : MonoBehaviour
{
    private XRGrabInteractable grabbable;
    public EnableSlice baseEnableSlice; 
    private readonly string layerName = "Interactable"; 
    private DeleteSliceOnButtonPress baseDeleteSliceOnButtonPress;

    public GameObject heartTarget;
    public Material crossSectionMaterial;

    public Transform planeCoordinates;
    public Rigidbody heartRigidBody;

    private void Start()
    {
        grabbable = GetComponent<XRGrabInteractable>();
        grabbable.activated.AddListener(SliceOnActivate);

        baseDeleteSliceOnButtonPress = GetComponent<DeleteSliceOnButtonPress>();    

        heartRigidBody = GetComponent<Rigidbody>(); 
    }

    private void SliceOnActivate(ActivateEventArgs activateEventArgs) 
    {
        Slice(heartTarget); 
    }
    public void Slice(GameObject target)
    {
        SlicedHull hull = target.Slice(planeCoordinates.position, planeCoordinates.up);

        if (hull != null) 
        {
            // upper hull
            GameObject upperHull = hull.CreateUpperHull(target, crossSectionMaterial);
            SliceComponentSetup(upperHull, true, target.name);
            upperHull.transform.position = new Vector3(heartTarget.transform.position.x + 0.1f, heartTarget.transform.position.y, heartTarget.transform.position.z + 0.1f);

            // lower hull
            GameObject lowerHull = hull.CreateLowerHull(target, crossSectionMaterial);
            SliceComponentSetup(lowerHull, false, target.name);
            upperHull.transform.position = new Vector3(heartTarget.transform.position.x + 0.1f, heartTarget.transform.position.y - 0.1f, heartTarget.transform.position.z + 0.1f);
        }
    }

    public void SliceComponentSetup(GameObject sliceComponent, bool upper, string baseName)
    {
        // set grabbable settings
        XRGrabInteractable sliceGrabbable = sliceComponent.AddComponent<XRGrabInteractable>();
        sliceGrabbable.activated.AddListener(SliceOnActivate); 

        // set delete on slice
        DeleteSliceOnButtonPress currentDeleteSliceOnButtonPressSettings = sliceComponent.AddComponent<DeleteSliceOnButtonPress>();
        currentDeleteSliceOnButtonPressSettings.deleteButton = baseDeleteSliceOnButtonPress.deleteButton;

        // set enable slice 
        EnableSlice currentEnableSlice = sliceComponent.AddComponent<EnableSlice>();

        currentEnableSlice.heartTarget = sliceComponent; 

        currentEnableSlice.crossSectionMaterial = baseEnableSlice.crossSectionMaterial;

        currentEnableSlice.planeCoordinates = baseEnableSlice.planeCoordinates;

        currentEnableSlice.heartRigidBody = baseEnableSlice.heartRigidBody;

        // set rigid boy 
        heartRigidBody = sliceComponent.AddComponent<Rigidbody>();

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
}
