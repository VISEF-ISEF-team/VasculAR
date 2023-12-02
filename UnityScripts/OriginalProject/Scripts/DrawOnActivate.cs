using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using Unity.XR.CoreUtils;
using UnityEditor;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit; 
public class DrawOnActivate : MonoBehaviour
{
    [SerializeField] GameObject paintBrush;
    [SerializeField] GameObject spherePrefab;
    [SerializeField] Transform brushTip;
    [SerializeField] public MeshRenderer otherSphereMeshRenderer; 
    private bool isActivate = false; 
    private void Start()
    {
        XRGrabInteractable grabbable = GetComponent<XRGrabInteractable>();
        grabbable.activated.AddListener(OnActivate);
        grabbable.deactivated.AddListener(OnDeactivate);
        grabbable.selectExited.AddListener(OnSelectExit);
    }

    private void Update()
    {
        if (isActivate == true)
        {
            DrawParticles();
        }
    }
  
    private void OnActivate(ActivateEventArgs activateArgs)
    {
        isActivate = true;
    }

    private void OnDeactivate(DeactivateEventArgs deactivateArgs)
    {
        isActivate = false;
    }
    private void OnSelectExit(SelectExitEventArgs selectExitArgs)
    {
        isActivate = false; 
    }
    private void DrawParticles()
    {
        Color otherSphereColor = otherSphereMeshRenderer.material.color;
        spherePrefab.GetComponent<MeshRenderer>().material.SetColor("New Color", otherSphereColor); 
        Instantiate(spherePrefab, brushTip.position, Quaternion.identity);
    }
}
