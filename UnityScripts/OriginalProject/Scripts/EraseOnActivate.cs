using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using Unity.XR.CoreUtils;
using UnityEditor;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit;

public class EraseOnActivate : MonoBehaviour
{
    private bool isActivate = false;
    private string prefabTag = "Sphere Prefab";
    private BoxCollider boxCollider;
    private Color highLightColor =  new Color(1.0f, 0.82f, 0.35f, 1.0f); 

    private void Start()
    {
        XRGrabInteractable grabbable = GetComponent<XRGrabInteractable>();
        grabbable.activated.AddListener(OnActivate);
        grabbable.deactivated.AddListener(OnDeactivate);
        boxCollider = GetComponent<BoxCollider>();
    }

    private void OnActivate(ActivateEventArgs activateEventArgs)
    {
        isActivate = true;
        boxCollider.isTrigger = true;
    }

    private void OnDeactivate(DeactivateEventArgs deactivateEventArgs) 
    {
        isActivate = false;
        boxCollider.isTrigger = false; 
    }



    private void OnTriggerEnter(Collider other)
    {
        if (isActivate == true)
        { 
            if (other.gameObject.CompareTag(prefabTag))
            {
                Destroy(other.gameObject); 
            }
        }
        else
        {
            MeshRenderer otherRenderer = other.GetComponent<MeshRenderer>();   
            if (otherRenderer != null) 
            {
                otherRenderer.material.color = highLightColor;
            }
        }
    }
}
