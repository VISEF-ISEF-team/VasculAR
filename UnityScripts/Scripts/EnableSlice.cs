using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using EzySlice;
using UnityEngine.XR.Interaction.Toolkit; 

public class EnableSlice : MonoBehaviour
{
    private XRGrabInteractable grabbable;
    private string layerName = "Interactable"; 

    [SerializeField] GameObject heartTarget;
    [SerializeField] Material crossSectionMaterial;

    public Transform planeCoordinates;
    public RayInteractorSettingsForGrabAndAnchor rayInteractorSettings;
    public DeleteSliceOnButtonPress deleteSliceOnButtonPressSettings;
    public Rigidbody heartRigidBody;
    private void Start()
    {
        grabbable = GetComponent<XRGrabInteractable>();
        grabbable.activated.AddListener(SliceOnActivate);
        heartRigidBody = GetComponent<Rigidbody>(); 
    }

    private void Update()
    {

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
            GameObject upperHull = hull.CreateUpperHull(target, crossSectionMaterial);
            SliceComponentSetup(upperHull);
            upperHull.transform.position = new Vector3(heartTarget.transform.position.x + 0.1f, heartTarget.transform.position.y, heartTarget.transform.position.z + 0.1f); 
        }
    }

    public void SliceComponentSetup(GameObject sliceComponent)
    {
        grabbable = sliceComponent.AddComponent<XRGrabInteractable>();
        rayInteractorSettings = sliceComponent.AddComponent<RayInteractorSettingsForGrabAndAnchor>(); 
        deleteSliceOnButtonPressSettings = sliceComponent.AddComponent<DeleteSliceOnButtonPress>();
        heartRigidBody = sliceComponent.AddComponent<Rigidbody>();
        sliceComponent.layer = LayerMask.NameToLayer(layerName); 
    }
}
