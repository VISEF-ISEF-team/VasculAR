using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class RayInteractorSettingsForGrabAndAnchor : ScriptableObject
{
    private XRRayInteractor leftRayInteractor;
    private XRRayInteractor rightRayInteractor;

    public void StartScript()
    {
        leftRayInteractor = GameObject.Find("LeftGrabRay").GetComponent<XRRayInteractor>();
        rightRayInteractor = GameObject.Find("RightGrabRay").GetComponent<XRRayInteractor>();
    }

    public void SetAnchorAndForceGrab(bool rightAnchor, bool leftAnchor, bool rightForceGrab, bool leftForceGrab)
    {
        leftRayInteractor.allowAnchorControl = leftAnchor;
        leftRayInteractor.useForceGrab = leftForceGrab;

        rightRayInteractor.allowAnchorControl = rightAnchor;
        rightRayInteractor.useForceGrab = rightForceGrab; 
    }

    public void SetAnchorAndForceGrabReverse()
    {
        leftRayInteractor.allowAnchorControl = !leftRayInteractor.allowAnchorControl;
        leftRayInteractor.useForceGrab = !leftRayInteractor.useForceGrab;

        rightRayInteractor.allowAnchorControl = !rightRayInteractor.allowAnchorControl;
        rightRayInteractor.useForceGrab = !rightRayInteractor.useForceGrab; 
    }
}
