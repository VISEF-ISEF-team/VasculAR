using UnityEngine;

public class SlicerCanvasManagerScript : MonoBehaviour
{
    [SerializeField] GameObject slicerObject; 
    [SerializeField] private MeshRenderer slicerPlaneRenderer;
    [SerializeField] float minScale = 0.1f; 
    [SerializeField] float maxScale = 1.0f;
    private SlicerSpawnOnUIControl slicerSpawnUIControl;
    float oldXScale;
    float oldYScale;
    float oldZScale; 

    private void Awake()
    {
        slicerSpawnUIControl = slicerObject.GetComponent<SlicerSpawnOnUIControl>();
    }

    private void OnEnable()
    {
        slicerObject.SetActive(true);
        slicerSpawnUIControl.SpawnSlicer();
        oldXScale = slicerObject.transform.localScale.x;
        oldYScale = slicerObject.transform.localScale.y;
        oldZScale = slicerObject.transform.localScale.z;

        Debug.Log($"{oldXScale} - {oldYScale} - {oldZScale}"); 
    }

    private void OnDisable()
    {
        slicerObject.SetActive(false); 
    }

    public void OnSliderChangeWidth(float widthScaleValue)
    {
        widthScaleValue = Mathf.Clamp(widthScaleValue, minScale, maxScale);
        slicerObject.transform.localScale = new Vector3(widthScaleValue, oldYScale, oldZScale);

        oldXScale = widthScaleValue; 
    }

    public void OnSliderChangeHeight(float heightScaleValue)
    {
        heightScaleValue = Mathf.Clamp(heightScaleValue, minScale, maxScale);
        slicerObject.transform.localScale = new Vector3(oldXScale, oldYScale, heightScaleValue);

        oldZScale = heightScaleValue;
    }

/*    public void OnSliderChangeTransparency(float transparencyValue)
    {
        // alpha value goes from 0 - 255 => go from 10 - 255 on slider value range

        Color oldColor = slicerPlaneRenderer.material.color;
        Color newColor = new Color(oldColor.r, oldColor.g, oldColor.b, transparencyValue);

        slicerPlaneRenderer.material.color = newColor; 
    }*/
}
