using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class RayInteractorSettingsForGrabAndAnchor : ScriptableObject
{
    private XRRayInteractor leftRayInteractor;
    private XRRayInteractor rightRayInteractor;

    private void Awake()
    {
        GameObject leftGrabRay = GameObject.Find("XR Origin (XR Rig)/Camera Offset/Left Grab Ray");
        GameObject rightGrabRay = GameObject.Find("XR Origin (XR Rig)/Camera Offset/Right Grab Ray");

        if (leftGrabRay != null) 
        {
            leftRayInteractor = leftGrabRay.GetComponent<XRRayInteractor>();
        }

        if (rightGrabRay != null)
        {
            rightRayInteractor = rightGrabRay.GetComponent<XRRayInteractor>();    
        }
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

    public bool IsHoveringOverUI()
    {
        bool res = false;
        if (leftRayInteractor.IsOverUIGameObject()) res = true;
        else if (rightRayInteractor.IsOverUIGameObject()) res = true;
        return res; 
    }
}
