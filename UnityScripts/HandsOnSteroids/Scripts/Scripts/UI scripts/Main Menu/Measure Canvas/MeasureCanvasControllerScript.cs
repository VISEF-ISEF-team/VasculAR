using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using UnityEngine.Rendering;

public class MeasureCanvasControllerScript : MonoBehaviour
{
    [SerializeField] GameObject measureObject;
    [SerializeField] Slider scaleSlider;

    private MeasureObjectActionScript measureObjectActionScript;
    private float maxScale = 0.2f; 
    private float minScale = 0.05f;

    private List<GameObject> measurePointList; 
    private void Start()
    {
        measureObjectActionScript = measureObject.GetComponent<MeasureObjectActionScript>();
        scaleSlider.value = 0.1f;
        scaleSlider.onValueChanged.AddListener(OnSliderChangeSphereSize); 
    }

    private void Update()
    {
        
    }

    private void OnEnable()
    {
        measureObject.SetActive(true);
        measurePointList = measureObjectActionScript.MeasurePointList; 
    }

    private void OnDisable()
    {
        measureObject.SetActive(false);
        measurePointList.Clear(); 
    }

    public void OnAllowLeftHandToggle(bool value)
    {
        measureObjectActionScript.AllowLeftHand = value; 
    }

    public void OnShowMeasurementToggle(bool value)
    {
        if (value == false)
        {
            foreach (var points in measurePointList)
            {
                points.GetComponent<MeasurePointActionScript>().endSphere.SetActive(false); 
                points.SetActive(false); 
            }
        }
        else if (value == true)
        {
            foreach (var points in measurePointList)
            {
                points.GetComponent<MeasurePointActionScript>().endSphere.SetActive(true);
                points.SetActive(true);
            }
        }
    }
    public void OnSliderChangeSphereSize(float scale)
    {
        scale = Mathf.Clamp(scale, maxScale, minScale);
        measureObjectActionScript.MeasurePointScale = new Vector3(scale, scale, scale); 
    }
}
