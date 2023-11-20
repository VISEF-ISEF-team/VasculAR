using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class RayInteractorSettingsForGrabAndAnchor : MonoBehaviour
{
    [SerializeField] private GameObject leftGrabRay;
    [SerializeField] private GameObject rightGrabRay;

    private XRRayInteractor leftRayInteractor;
    private XRRayInteractor rightRayInteractor;

    private void Start()
    {
        leftRayInteractor = leftGrabRay.GetComponent<XRRayInteractor>();
        rightRayInteractor = rightGrabRay.GetComponent<XRRayInteractor>();
        SetAnchorAndForceGrab(true, true, false, false);
    }

    public void SetAnchorAndForceGrab(bool rightAnchor, bool leftAnchor, bool rightForceGrab, bool leftForceGrab)
    {
        leftRayInteractor.allowAnchorControl = leftAnchor;
        leftRayInteractor.useForceGrab = leftForceGrab;

        rightRayInteractor.allowAnchorControl = rightAnchor;
        rightRayInteractor.useForceGrab = rightForceGrab; 
    }
}
