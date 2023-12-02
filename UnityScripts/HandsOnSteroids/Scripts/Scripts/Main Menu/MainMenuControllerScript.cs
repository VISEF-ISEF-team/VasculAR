using System;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR.Interaction.Toolkit; 

public class MainMenuControllerScript : MonoBehaviour
{
    [SerializeField] InputActionProperty menuButton;
    [SerializeField] GameObject mainMenuCanvas; 
    private GetHeadPosition getHeadPosition;
    private RayInteractorSettingsForGrabAndAnchor rayInteractorSettings;
    private bool mainMenuCanvasActiveState = false;
    private XRGrabInteractable uiGrabbable;

    // Get all tools reference 
    [SerializeField] GameObject paintBrush;
    [SerializeField] GameObject eraser;
    [SerializeField] GameObject slicer; 
    private void Start()
    {
        getHeadPosition = ScriptableObject.CreateInstance<GetHeadPosition>();
        getHeadPosition.StartScript(); 
        rayInteractorSettings = ScriptableObject.CreateInstance<RayInteractorSettingsForGrabAndAnchor>();
        rayInteractorSettings.StartScript();
        uiGrabbable = GetComponent<XRGrabInteractable>();
        uiGrabbable.hoverEntered.AddListener(OnUIHoverEnter);
        uiGrabbable.hoverExited.AddListener(OnUIHoverExit);
        uiGrabbable.selectEntered.AddListener(OnUISelectEnter);
        uiGrabbable.selectExited.AddListener(OnUISelectExit); 
    }

    private void Update()
    {
        if (menuButton.action.WasPressedThisFrame())
        {
            mainMenuCanvas.SetActive(!mainMenuCanvasActiveState); 
            mainMenuCanvasActiveState = !mainMenuCanvasActiveState;
            transform.position = getHeadPosition.TransformPositionInFrontOfHead();
            transform.LookAt(getHeadPosition.TransformToLookAt(transform.position.y));
            mainMenuCanvas.transform.forward *= -1; 
        }
    }
    private void OnUIHoverExit(HoverExitEventArgs arg0)
    {
        rayInteractorSettings.SetAnchorAndForceGrab(false, false, false, false); 
    }

    private void OnUIHoverEnter(HoverEnterEventArgs arg0)
    {
        rayInteractorSettings.SetAnchorAndForceGrab(true, true, true, true); 
    }
    private void OnUISelectExit(SelectExitEventArgs arg0)
    {
        rayInteractorSettings.SetAnchorAndForceGrab(false, false, false, false);
    }

    private void OnUISelectEnter(SelectEnterEventArgs arg0)
    {
        rayInteractorSettings.SetAnchorAndForceGrab(true, true, true, true);
    }

    // have a list of events to set the tools to active
    public void SetPaintBrushActive(bool value)
    {
        paintBrush.SetActive(value); 
    }
    public void SetEraserActive(bool value)
    {
        eraser.SetActive(value);
    }
    public void SetSlicerActive(bool value)
    {
        slicer.SetActive(value);    
    }
}
