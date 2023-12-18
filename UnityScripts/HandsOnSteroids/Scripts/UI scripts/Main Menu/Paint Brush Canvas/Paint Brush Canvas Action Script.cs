using UnityEngine;
using UnityEngine.UI;

public class PaintBrushCanvasActionScript : MonoBehaviour
{
    [SerializeField] GameObject paintBrush; 
    [SerializeField] GameObject changeThisSphere;
    [SerializeField] Slider sphereScaleSlider;

    private PaintBrushActionScript paintBrushScript;
    private float maxScale = 3.0f;
    private float minScale = 0.25f;
    private void OnEnable()
    {
        changeThisSphere.transform.localScale = changeThisSphere.transform.InverseTransformDirection(Vector3.one);
        sphereScaleSlider.onValueChanged.AddListener(OnSliderChangeSphereSize);
        paintBrush.SetActive(true); 
    }
    private void OnDisable()
    {
        paintBrush.SetActive(false);
    }
    private void Start()
    {
        paintBrushScript = paintBrush.GetComponent<PaintBrushActionScript>();
        sphereScaleSlider.value = 1.0f; 
    }

    public void OnSliderChangeSphereSize(float scale)
    {
        scale = Mathf.Clamp(scale, maxScale, minScale);
        changeThisSphere.transform.localScale = changeThisSphere.transform.InverseTransformDirection(new Vector3(scale, scale, scale));
        paintBrushScript.RealSphereSize = new Vector3(scale, scale, scale);  
    }

    public void OnAllowLeftHandButtonPress(bool isOn)
    {
        paintBrushScript.AllowLeftHand = isOn;
    }
}
