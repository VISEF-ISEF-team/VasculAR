using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit;

public class SliceActionScript : MonoBehaviour
{
    [SerializeField] private GameObject leftGrabRay;
    [SerializeField] private GameObject rightGrabRay;

    private XRRayInteractor leftRayInteractor;
    private XRRayInteractor rightRayInteractor;

    public ActionBasedContinuousMoveProvider actionBasedContinuousMoveProvider;
    public ActionBasedContinuousTurnProvider actionBasedContinuousTurnProvider; 

    public InputActionProperty editSizeButton;
    [SerializeField] InputActionProperty leftHandMoveAction;
    [SerializeField] InputActionProperty rightHandMoveAction;

    [SerializeField] float scaleSpeed = 0.1f;
    [SerializeField] float minScale = 0.01f;
    [SerializeField] float maxScale = 2.0f; 
    

    public Transform planeTransform; 

    
    private void Start()
    {
        XRGrabInteractable grabbable = GetComponent<XRGrabInteractable>();
        grabbable.selectEntered.AddListener(OnSelectEnter);
        grabbable.selectExited.AddListener(OnSelectExit); 

        leftRayInteractor = leftGrabRay.GetComponent<XRRayInteractor>();    
        rightRayInteractor = rightGrabRay.GetComponent<XRRayInteractor>();

        
    }

    private void Update() 
    { 
        if (editSizeButton.action.WasPressedThisFrame())
        {
            actionBasedContinuousMoveProvider.enabled = false; 
            actionBasedContinuousTurnProvider.enabled = false;

            // left hand is use to control the x axis
            Vector2 leftHandVector = leftHandMoveAction.action?.ReadValue<Vector2>() ?? Vector2.zero; 
            // right hand is use to control the z axis
            Vector2 rightHandVector = rightHandMoveAction.action?.ReadValue<Vector2>() ?? Vector2.zero;
            
            float newScaleX = Mathf.Clamp(planeTransform.localScale.x + leftHandVector.x * scaleSpeed, minScale, maxScale);
            float newScaleY = planeTransform.localScale.y; 
            float newScaleZ = Mathf.Clamp(planeTransform.localScale.z + leftHandVector.y * scaleSpeed, minScale, maxScale);

            transform.localScale = new Vector3(newScaleX, newScaleY, newScaleZ); 
        }
    }

    private void OnSelectEnter(SelectEnterEventArgs selectEnterEventArgs) 
    {
        leftRayInteractor.allowAnchorControl = true;
        leftRayInteractor.useForceGrab = false; 

        rightRayInteractor.allowAnchorControl = true;
        rightRayInteractor.useForceGrab = false;
    }

    private void OnSelectExit(SelectExitEventArgs selectExitEventArgs)
    {
        leftRayInteractor.allowAnchorControl = false;
        leftRayInteractor.useForceGrab = true;

        rightRayInteractor.allowAnchorControl = false;
        rightRayInteractor.useForceGrab = true; 

    }
}
