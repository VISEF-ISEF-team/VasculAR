using UnityEngine;
using UnityEngine.InputSystem.Android;
using UnityEngine.UI;

public class MeasureCanvasControllerScript : MonoBehaviour
{
    [SerializeField] GameObject measureObject;
    [SerializeField] Slider scaleSlider;

    private MeasureObjectActionScript measureObjectActionScript;
    private float maxScale = 0.2f; 
    private float minScale = 0.05f;
    private Button deleteButton;
    private bool isPressed = false;
    private Color normalColor = new Color(0 / 255.0f, 253 / 255.0f, 241 / 255.0f, 120 / 255.0f);
    private Color pressedColor = new Color(0 / 255.0f, 147 / 255.0f, 140 / 255.0f, 255 / 255.0f);

    private void Start()
    {
        measureObjectActionScript = measureObject.GetComponent<MeasureObjectActionScript>();
        scaleSlider.value = 0.1f;
        scaleSlider.onValueChanged.AddListener(OnSliderChangeSphereSize);
        deleteButton = GetComponentInChildren<Button>();
        deleteButton.onClick.AddListener(OnDeleteButtonPress);
    }

    private void OnEnable()
    {
        measureObject.SetActive(true);
        measureObjectActionScript.SetGrabStatusForMeasurePoints(true); 
    }

    private void OnDisable()
    {
        measureObject.SetActive(false);
        measureObjectActionScript.SetGrabStatusForMeasurePoints(false); 
    }

    public void OnAllowLeftHandToggle(bool value)
    {
        measureObjectActionScript.AllowLeftHand = value; 
    }

    public void OnShowMeasurementToggle(bool value)
    {
        if (value == false)
        {
            foreach (var points in measureObjectActionScript.MeasurePointList)
            {
                points.GetComponent<MeasurePointActionScript>().endSphere.SetActive(false); 
                points.SetActive(false); 
            }
        }
        else if (value == true)
        {
            foreach (var points in measureObjectActionScript.MeasurePointList)
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

    public void OnDeleteButtonPress()
    {
        isPressed = !isPressed; 
        if (isPressed)
        {
            Image buttonImage = deleteButton.GetComponent<Image>(); 
            buttonImage.color = pressedColor; 
        }
        else
        {
                Image buttonImage = deleteButton.GetComponent<Image>();
            buttonImage.color = normalColor;    
        }
    }
}
