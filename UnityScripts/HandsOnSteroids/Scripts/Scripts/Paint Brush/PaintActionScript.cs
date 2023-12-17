using UnityEngine;
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
        selfInteractable.activated.AddListener(OnActivate);
        selfInteractable.deactivated.AddListener(OnDeactivate); 
        selfMeshRenderer = GetComponent<MeshRenderer>();    
        selfSphereColor = selfMeshRenderer.material.color;
    }

    private void OnHoverEnter(HoverEnterEventArgs arg0)
    {
        selfMeshRenderer.material.color = highlightColor;
    }
    private void OnHoverExit(HoverExitEventArgs arg0)
    {
        selfMeshRenderer.material.color = selfSphereColor;
    }

    private void OnDeactivate(DeactivateEventArgs arg0)
    {
        if (gameObject != null)
        {
            Destroy(gameObject); 
        }
    }

    private void OnActivate(ActivateEventArgs arg0)
    {
        Destroy(gameObject); 
    }
}

