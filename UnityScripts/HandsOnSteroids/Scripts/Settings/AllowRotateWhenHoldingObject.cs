using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.InputSystem;

public class AllowRotateWhenHoldingObject : MonoBehaviour
{
    [SerializeField] XRRayInteractor leftRayInteractor;
    [SerializeField] XRRayInteractor rightRayInteractor;
    [SerializeField] InputActionProperty allowRotateButton;

    private XRGrabInteractable selfGrabbable; 

    private bool allowAnchorControlField = true;
    private bool isSelect; 

    private void Start()
    {
        selfGrabbable = GetComponent<XRGrabInteractable>();
        selfGrabbable.selectEntered.AddListener(OnSelectEnter);
        selfGrabbable.selectExited.AddListener(OnSelectExit); 
    }

    private void Update()
    {
        if (allowRotateButton.action.WasPressedThisFrame() && isSelect)
        {
            leftRayInteractor.allowAnchorControl = allowAnchorControlField;
            rightRayInteractor.allowAnchorControl = allowAnchorControlField;
            allowAnchorControlField = !allowAnchorControlField;
        }
    }

    private void OnSelectEnter(SelectEnterEventArgs selectEnterEventArgs)
    {
        isSelect = true; 
    }

    private void OnSelectExit(SelectExitEventArgs selectExitedEventArgs) 
    {
        isSelect = false;

        leftRayInteractor.allowAnchorControl = false;
        rightRayInteractor.allowAnchorControl = false; 
    }
}
