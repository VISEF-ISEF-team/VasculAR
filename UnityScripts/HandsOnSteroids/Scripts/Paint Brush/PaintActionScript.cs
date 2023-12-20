using System;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.XR.Interaction.Toolkit;

public class PaintActionScript : MonoBehaviour
{
    [SerializeField] Color highlightColor;
    private XRSimpleInteractable selfInteractable;
    private Color selfSphereColor;
    private MeshRenderer selfMeshRenderer;
    private bool allowDelete;
    
    private void Start()
    {
        selfInteractable = GetComponent<XRSimpleInteractable>();
        selfInteractable.hoverEntered.AddListener(OnHoverEnter);
        selfInteractable.hoverExited.AddListener(OnHoverExit);
        selfInteractable.selectEntered.AddListener(OnSelectEntered);
        selfInteractable.selectExited.AddListener(OnSelectExit); 
        selfMeshRenderer = GetComponent<MeshRenderer>();    
        selfSphereColor = selfMeshRenderer.material.color;
    }

    private void OnSelectEntered(SelectEnterEventArgs arg0)
    {
        Destroy(gameObject); 
    }

    private void OnSelectExit(SelectExitEventArgs arg0)
    {
        if (gameObject != null)
        {
            Destroy(gameObject);
        }
    }

    private void OnHoverEnter(HoverEnterEventArgs arg0)
    {
        selfMeshRenderer.material.color = highlightColor;
    }
    private void OnHoverExit(HoverExitEventArgs arg0)
    {
        selfMeshRenderer.material.color = selfSphereColor;
    }
}

