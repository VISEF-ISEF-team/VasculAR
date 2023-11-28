using System.Collections;
using System.Collections.Generic;
using UnityEngine.InputSystem;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit; 

public class SpawnOnButtonPress : MonoBehaviour
{
    public Transform head;
    public GameObject planeObject;
    private float spawnDistance = 2.0f;
    private float spawnYAxisOffset = 0.25f;
    //private XRGrabInteractable interactable;
    [SerializeField] InputActionProperty spawnButton;

    private void Start()
    {
        //interactable = GetComponent<XRGrabInteractable>();  
    }
    private void Update()
    {
        if (spawnButton.action.WasPressedThisFrame())
        {
            planeObject.SetActive(!planeObject.activeSelf);
            transform.position = head.position + new Vector3(head.forward.x, spawnYAxisOffset, head.forward.z).normalized * spawnDistance;
        }
    }
}
