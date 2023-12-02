using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR.Interaction.Toolkit;

public class SlicerUIConfigManager : MonoBehaviour
{
    // reference the original slicer object 
    public GameObject slicerObject; 

    [SerializeField] private XRRayInteractor leftRayInteractor;
    [SerializeField] private XRRayInteractor rightRayInteractor;
    [SerializeField] GameObject slicerUIConfigObject;
    private XRGrabInteractable uiGrabbable;
    private XRGrabInteractable slicerObjectGrabInteractable;

    private GetHeadPosition getHeadPosition; 
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
        getHeadPosition = ScriptableObject.CreateInstance<GetHeadPosition>();
        getHeadPosition.StartScript(); 
    }

    private void Update()
    {
        if (editSizeButton.action.WasPressedThisFrame() && isSelect)
        {
            slicerUIConfigObject.SetActive(!slicerUIConfigObject.activeSelf);
            slicerUIConfigObject.transform.position = getHeadPosition.TransformPositionInFrontOfHead();
            slicerUIConfigObject.transform.LookAt(getHeadPosition.TransformToLookAt(slicerUIConfigObject.transform.position.y)); 
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
