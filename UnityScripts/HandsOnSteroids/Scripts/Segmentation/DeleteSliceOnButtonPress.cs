using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR.Interaction.Toolkit;

public class DeleteSliceOnButtonPress : MonoBehaviour
{
    private XRGrabInteractable sliceGrabbable;
    public InputActionProperty deleteButton;
    private bool allowDelete = false;

    private void Start()
    {
        sliceGrabbable = GetComponent<XRGrabInteractable>();    
        if (sliceGrabbable != null)
        {
            sliceGrabbable.selectEntered.AddListener(OnSelectEnter);
            sliceGrabbable.selectExited.AddListener(OnSelectExit);
        }
    }

    private void OnSelectExit(SelectExitEventArgs arg0)
    {
        allowDelete = false;
    }

    private void OnSelectEnter(SelectEnterEventArgs arg0)
    {
        allowDelete = true;
    }

    private void Update()
    {
        if (allowDelete && deleteButton.action.WasPressedThisFrame())
        {
            Destroy(gameObject);
        }
    }
}
