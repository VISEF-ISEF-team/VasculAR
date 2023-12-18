using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit; 

public class MainMenuControllerScript : MonoBehaviour
{
    [SerializeField] InputActionProperty menuButton;
    [SerializeField] GameObject mainCanvas;

    private GetHeadPosition getHeadPosition;
    private RayInteractorSettingsForGrabAndAnchor rayInteractorSettings;
    private bool mainMenuCanvasActiveState = false;
    private XRGrabInteractable uiGrabbable;

    [SerializeField] GameObject mainMenuCanvas;
    [SerializeField] GameObject paintBrushCanvas;
    [SerializeField] GameObject slicerCanvas;
    [SerializeField] GameObject measureCanvas;
    [SerializeField] GameObject segmentationCanvas; 
    
    private Stack<int> forwardStack; 
    private Stack<int> backwardStack;
    private int currentlyActiveIndex;
    private List<GameObject> menuCanvasManager; 

    // UI references
    [SerializeField] Button forwardButton;
    [SerializeField] Button backwardButton;
    private void Start()
    {
        rayInteractorSettings = ScriptableObject.CreateInstance<RayInteractorSettingsForGrabAndAnchor>();
        rayInteractorSettings.StartScript();
        uiGrabbable = GetComponent<XRGrabInteractable>();
        uiGrabbable.hoverEntered.AddListener(OnUIHoverEnter);
        uiGrabbable.hoverExited.AddListener(OnUIHoverExit);
        uiGrabbable.selectEntered.AddListener(OnUISelectEnter);
        uiGrabbable.selectExited.AddListener(OnUISelectExit); 
        getHeadPosition = GetHeadPosition.GetHeadPositionReference();
        forwardStack = new Stack<int>(); 
        backwardStack = new Stack<int>();

        forwardButton.onClick.AddListener(OnForwardButtonPress);
        backwardButton.onClick.AddListener(OnBackwardButtonPress);
        menuCanvasManager = new List<GameObject>()
        {
            mainMenuCanvas,
            paintBrushCanvas,
            slicerCanvas,
            measureCanvas,
            segmentationCanvas,
        };
        currentlyActiveIndex = 0;
    }

    private void Update()
    {
        if (menuButton.action.WasPressedThisFrame())
        {
            mainCanvas.SetActive(!mainMenuCanvasActiveState);
            Reposition(); 
        }

        CheckStackStatus();
    }

    private void Reposition()
    {
        mainMenuCanvasActiveState = !mainMenuCanvasActiveState;
        transform.position = getHeadPosition.TransformPositionInFrontOfHead();
        transform.LookAt(getHeadPosition.TransformToLookAt(transform.position.y));
        mainCanvas.transform.forward *= -1;
    }

    // XR Grab Interactable Listeners
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

    // Check stack status
    private void CheckStackStatus()
    {
        if (forwardStack.Count > 0) forwardButton.interactable = true;
        else forwardButton.interactable = false;

        if (backwardStack.Count > 0) backwardButton.interactable = true;
        else backwardButton.interactable = false;   
    }
    public void OnForwardButtonPress()
    {
        int top = forwardStack.Pop(); 
        backwardStack.Push(currentlyActiveIndex);
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        menuCanvasManager[top].SetActive(true);
        currentlyActiveIndex = top; 
    }
    public void OnBackwardButtonPress()
    {
        int top = backwardStack.Pop(); 
        forwardStack.Push(currentlyActiveIndex);
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        menuCanvasManager[top].SetActive(true);
        currentlyActiveIndex = top; 
    }

    public void OnSelectToolButtonPress()
    {
        // index of main menu is 0
        if (currentlyActiveIndex != 0)
        {
            menuCanvasManager[currentlyActiveIndex].SetActive(false);
            backwardStack.Push(currentlyActiveIndex);
            menuCanvasManager[0].SetActive(true);
            currentlyActiveIndex = 0;
        }
    }

    public void OnPaintBrushCanvasButtonPress()
    {
        // index in manager is 1
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        backwardStack.Push(currentlyActiveIndex); 
        menuCanvasManager[1].SetActive(true);
        currentlyActiveIndex = 1;
    }

    public void OnSlicerCanvasButtonPress()
    {
        // index in manager is 2
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        backwardStack.Push(currentlyActiveIndex);
        menuCanvasManager[2].SetActive(true);
        currentlyActiveIndex = 2;
    }

    public void OnMeasureCanvasButtonPress()
    {
        // index in manager is 3
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        backwardStack.Push(currentlyActiveIndex);
        menuCanvasManager[3].SetActive(true);
        currentlyActiveIndex = 3;
    }

    public void OnSegmentCanvasButtonPress()
    {
        // index in manager is 4
        menuCanvasManager[currentlyActiveIndex].SetActive(false);
        backwardStack.Push(currentlyActiveIndex);
        menuCanvasManager[4].SetActive(true);
        currentlyActiveIndex = 4;
    }
}
