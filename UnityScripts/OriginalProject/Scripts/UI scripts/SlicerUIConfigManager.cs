using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR.Interaction.Toolkit;

public class SlicerUIConfigManager : MonoBehaviour
{
    // reference the original slicer object 
    public UIConfigs uiConfigs;
    public GameObject slicerObject; 

    [SerializeField] private XRRayInteractor leftRayInteractor;
    [SerializeField] private XRRayInteractor rightRayInteractor;
    [SerializeField] GameObject slicerUIConfigObject;
    private XRGrabInteractable uiGrabbable;
    private XRGrabInteractable slicerObjectGrabInteractable; 

    private Transform head;
    private float spawnDistance;
    private bool isSelect = false;
    public InputActionProperty editSizeButton;

    private void Start()
    {
        uiGrabbable = GetComponent<XRGrabInteractable>();
        uiGrabbable.hoverEntered.AddListener(OnUIHoverEnter);
        uiGrabbable.hoverExited.AddListener(OnUIHoverExit);

        slicerObjectGrabInteractable = GetComponent<XRGrabInteractable>();
        slicerObjectGrabInteractable.selectEntered.AddListener(OnSelectEnter);
        slicerObjectGrabInteractable.selectExited.AddListener(OnSelectExit);
        head = uiConfigs.headConfigObjectTransform;
        spawnDistance = uiConfigs.spawnDistance;
    }

    private void Update()
    {
        if (editSizeButton.action.WasPressedThisFrame() && isSelect)
        {
            slicerUIConfigObject.SetActive(!slicerUIConfigObject.activeSelf);
            slicerUIConfigObject.transform.position = uiConfigs.TransformPositionInFrontOfHead(head, spawnDistance);
            slicerUIConfigObject.transform.LookAt(new Vector3(head.position.x, slicerUIConfigObject.transform.position.y, head.position.z));
            slicerUIConfigObject.transform.forward *= -1;
        }
    }
    private void OnUIHoverEnter(HoverEnterEventArgs hoverEnterEventArgs)
    {
        leftRayInteractor.useForceGrab = false;
        rightRayInteractor.useForceGrab = false; 
    }

    private void OnUIHoverExit(HoverExitEventArgs hoverExitEventArgs) 
    {
        leftRayInteractor.useForceGrab = true;
        rightRayInteractor.useForceGrab = true; 
    }

    private void OnSelectEnter(SelectEnterEventArgs selectEnterEventArgs)
    {
        isSelect = true;
    }

    private void OnSelectExit(SelectExitEventArgs selectExitEventArgs)
    {
        isSelect = false;
    }

}
