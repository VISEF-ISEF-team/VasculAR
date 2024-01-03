using System.Collections;
using System.Collections.Generic;
using Unity.XR.CoreUtils;
using UnityEngine;
using UnityEngine.UI;

public class SegmentColorButtonControllerScript : MonoBehaviour
{
    public GameObject segmentObject;
    public string segmentName;
    public MeshRenderer otherSphereRenderer;
    public Material baseMaterial; 

    private Color oldColor;
    private MeshRenderer segmentObjectRenderer; 
    private bool isActive = false; 

    private void Start()
    {
        oldColor = segmentObjectRenderer.material.color; 
    }
    private void Update()
    {
        if (isActive)
        {
            Color currentColor = otherSphereRenderer.material.color; 
            if (currentColor != oldColor)
            {
                Material newMaterial = Instantiate(baseMaterial);
                newMaterial.color = currentColor; 
                segmentObjectRenderer.material = newMaterial;
                oldColor = currentColor; 
            }
        }
    }
    public void SetListener()
    {
        gameObject.GetComponent<Button>().onClick.AddListener(OnSegmentColorButtonPress); 
    }

    public void OnSegmentColorButtonPress()
    {
        isActive = !isActive; 
    }

}
