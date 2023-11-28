using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit;

public class ColorPickerManager : MonoBehaviour
{
    public GameObject colorPicker;
    public GameObject changeThisSphere; 
    public InputActionProperty showColorPicker;

    private GetHeadPosition getHeadPosition; 
    [SerializeField] private GameObject paintBrush;
    private bool willShowColorPicker = false; 

    private void Start()
    {
        XRGrabInteractable grabbable = paintBrush.GetComponent<XRGrabInteractable>();
        grabbable.selectEntered.AddListener(OnSelectEnter);
        grabbable.selectExited.AddListener(OnSelectExitColorPicker);
        getHeadPosition = ScriptableObject.CreateInstance<GetHeadPosition>();
        getHeadPosition.StartScript();
    }
    private void Update()
    {
        if (willShowColorPicker)
        {
            if (showColorPicker.action.WasPressedThisFrame()) 
            {
                colorPicker.SetActive(!colorPicker.activeSelf);
                changeThisSphere.SetActive(!changeThisSphere.activeSelf);   

                // Take position of head, move to the direction that the player is looking at then move it away with a multiplier of spawnDistance
                colorPicker.transform.position = getHeadPosition.TransformPositionInFrontOfHead(); 
            }

            colorPicker.transform.LookAt(getHeadPosition.TransformToLookAt(colorPicker.transform.position.y)); 

            // flip canvas so as not to be mirrored
            colorPicker.transform.forward *= -1;
        }
    }

    private void OnSelectEnter(SelectEnterEventArgs selectEnterEventArgs)
    {
        willShowColorPicker = true;
    }

    private void OnSelectExitColorPicker(SelectExitEventArgs selectExitEventArgs)
    {
        willShowColorPicker = false;
        if (colorPicker.activeSelf)
        {
            colorPicker.SetActive(false);   
        }
    }
}
