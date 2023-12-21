using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit; 

public class SlicerInteractorSettings : MonoBehaviour
{
    private XRGrabInteractable slicerGrabInteractable;
    [SerializeField] private XRRayInteractor leftRayInteractor;
    [SerializeField] private XRRayInteractor rightRayInteractor;
    private void Start()
    {
        slicerGrabInteractable = GetComponent<XRGrabInteractable>();
        slicerGrabInteractable.selectEntered.AddListener(OnSelectEnter);
        slicerGrabInteractable.selectExited.AddListener(OnSelectExit);
        slicerGrabInteractable.hoverEntered.AddListener(OnHoverEnter);
        slicerGrabInteractable.hoverExited.AddListener(OnHoverExit);
    }

    private void OnHoverExit(HoverExitEventArgs arg0)
    {
        leftRayInteractor.useForceGrab = false;
        rightRayInteractor.useForceGrab = false;
    }

    private void OnHoverEnter(HoverEnterEventArgs arg0)
    {
        leftRayInteractor.useForceGrab = false;
        rightRayInteractor.useForceGrab = false;
    }

    private void OnSelectExit(SelectExitEventArgs arg0)
    {
        leftRayInteractor.useForceGrab = false; 
        rightRayInteractor.useForceGrab = false;
    }

    private void OnSelectEnter(SelectEnterEventArgs arg0)
    {
        leftRayInteractor.useForceGrab = false;
        rightRayInteractor.useForceGrab = false; 
    }
}