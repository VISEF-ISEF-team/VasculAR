using UnityEngine;
using UnityEngine.Animations.Rigging;
using UnityEngine.UI;

public class PaintBrushCanvasActionScript : MonoBehaviour
{
    [SerializeField] GameObject paintBrush; 
    [SerializeField] GameObject changeThisSphere;
    [SerializeField] Slider sphereScaleSlider;

    private PaintBrushActionScript paintBrushScript;
    private float maxScale = 1.0f;
    private float minScale = 0.01f;

    private RayInteractorSettingsForGrabAndAnchor rayInteractorSettings; 

    private void OnEnable()
    {
        paintBrush.SetActive(true);
        rayInteractorSettings = ScriptableObject.CreateInstance<RayInteractorSettingsForGrabAndAnchor>();
    }

    private void OnDisable()
    {
        paintBrush.SetActive(false);
    }

    // scale is 0.001
    private void Start()
    {
        paintBrushScript = paintBrush.GetComponent<PaintBrushActionScript>();
        float currentVal = sphereScaleSlider.value;

        changeThisSphere.transform.localScale = new Vector3(currentVal * 1000, currentVal * 1000, currentVal * 1000);

        paintBrushScript.RealSphereSize = new Vector3(currentVal, currentVal, currentVal); 
    }

    private void Update()
    {
        if (rayInteractorSettings.IsHoveringOverUI())
        {
            paintBrushScript.allowDrawing = false; 
        }
        else if (paintBrushScript.allowDrawing == false)
        {
            paintBrushScript.allowDrawing = true;
        }
    }

    public void OnSliderChangeSphereSize(float scale)
    {
        scale = Mathf.Clamp(scale, minScale, maxScale);
        changeThisSphere.transform.localScale = new Vector3(scale * 1000, scale * 1000, scale * 1000);
        paintBrushScript.RealSphereSize = new Vector3(scale, scale, scale);
    }

    public void OnAllowLeftHandButtonPress(bool isOn)
    {
        paintBrushScript.AllowLeftHand = isOn;
    }

    public void OnAllowDeleteButton(bool allowDelete)
    {
        paintBrushScript.allowDrawing = !allowDelete; 
    }
}
