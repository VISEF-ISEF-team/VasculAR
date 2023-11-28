using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SlicerChangeSizeUIControl : MonoBehaviour
{
    [SerializeField] private MeshRenderer slicerPlaneRenderer;
    [SerializeField] float minScale = 0.1f; 
    [SerializeField] float maxScale = 3.0f;

    public void ChangeWidth(float widthScaleValue)
    {
        widthScaleValue = Mathf.Clamp(widthScaleValue, minScale, maxScale);
        transform.localScale = new Vector3(widthScaleValue, transform.localScale.y, transform.localScale.z);
    }

    public void ChangeHeight(float heightScaleValue)
    {
        heightScaleValue = Mathf.Clamp(heightScaleValue, minScale, maxScale);
        transform.localScale = new Vector3(transform.localScale.x, heightScaleValue, transform.localScale.z);
    }

    public void ChangeTransparency(float transparencyValue)
    {
        // alpha value goes from 0 - 255 => go from 10 - 255 on slider value range

        Color oldColor = slicerPlaneRenderer.material.color;
        Color newColor = new Color(oldColor.r, oldColor.g, oldColor.b, transparencyValue);

        slicerPlaneRenderer.material.color = newColor; 
    }
}
