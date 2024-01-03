using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit;

public class NewColorPickerControllerScript : MonoBehaviour
{
    [SerializeField] GameObject colorPanelObject;
    [SerializeField] RawImage hueImage; 
    [SerializeField] MeshRenderer sphereRenderer;
    [SerializeField] TextMeshProUGUI hexText;
    [SerializeField] XRRayInteractor leftRayInteractor;
    [SerializeField] XRRayInteractor rightRayInteractor;
    [SerializeField] GameObject colorPickerObject;
    [SerializeField] Camera xrCamera; 

    [SerializeField] InputActionProperty leftRayActivateButton;
    [SerializeField] InputActionProperty rightRayActivateButton;

    private RectTransform colorPanelTransform;
    private RawImage colorPanelImage;
    private Texture2D colorPanelTexture;
    private Texture2D hueTexture;
    private Image colorPickerImage; 

    private float currentHue;

    private float colorPanelWidth;
    private float colorPanelHeight;
    private Vector2 colorPanelCenterPosition; 

    private void Start()
    {
        colorPanelImage = colorPanelObject.GetComponent<RawImage>();
        colorPickerImage = colorPickerObject.GetComponent<Image>(); 
        colorPanelTransform = colorPanelObject.GetComponent<RectTransform>();

        colorPanelWidth = colorPanelTransform.rect.width; 
        colorPanelHeight = colorPanelTransform.rect.height;

        colorPanelCenterPosition = new Vector2(colorPanelWidth / 2, colorPanelHeight / 2);
        Debug.Log(colorPanelCenterPosition); 

        CreateHueImage(); 
        CreateSatValImage();
        UpdateColorPicker(); 
    }

    private void Update()
    {
        if (leftRayInteractor.IsOverUIGameObject())
        {
            if (leftRayInteractor.TryGetCurrentUIRaycastResult(out RaycastResult rayCastResult, out int raycastEndpointIndex))
            {
                if (leftRayActivateButton.action.WasPressedThisFrame())
                { 
                    if (rayCastResult.gameObject == colorPanelObject)
                    {
                        Vector2 screenPosition = rayCastResult.screenPosition;
                        RectTransformUtility.ScreenPointToLocalPointInRectangle(colorPanelTransform, screenPosition, xrCamera, out Vector2 localPosition);
                        Vector3 newColorPickerPosition = new Vector3(localPosition.x, localPosition.y, 1);
                        colorPickerObject.GetComponent<RectTransform>().anchoredPosition3D = newColorPickerPosition; 
                        colorPickerObject.transform.position = newColorPickerPosition;
                        UpdateColorPicker(); 
                    }
                }
            }

        }

        if (rightRayInteractor.IsOverUIGameObject())
        {
            if (rightRayInteractor.TryGetCurrentUIRaycastResult(out RaycastResult rayCastResult, out int raycastEndpointIndex))
            {
                if (rightRayActivateButton.action.WasPressedThisFrame())
                {
                    if (rayCastResult.gameObject == colorPanelObject)
                    {
                        Vector2 screenPosition = rayCastResult.screenPosition;
                        RectTransformUtility.ScreenPointToLocalPointInRectangle(colorPanelTransform, screenPosition, xrCamera, out Vector2 localPosition);
                        Vector3 newColorPickerPosition = new Vector3(localPosition.x, localPosition.y, 1);
                        colorPickerObject.GetComponent<RectTransform>().anchoredPosition3D = newColorPickerPosition;
                        UpdateColorPicker(); 
                    }
                }
            }

        }
    }

    private void CreateSatValImage()
    {
        colorPanelTexture = new Texture2D(16, 16);
        colorPanelTexture.wrapMode = TextureWrapMode.Clamp;

        float width = colorPanelTexture.width;
        float height = colorPanelTexture.height;

        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                Color newColor = Color.HSVToRGB(1, (float)i / width, (float)j / height);
                colorPanelTexture.SetPixel(i, j, newColor);
            }
        }

        colorPanelTexture.Apply();
        colorPanelImage.texture = colorPanelTexture;
    }
    private void CreateHueImage()
    {
        // Create a 1x16 texture for the hue gradient
        hueTexture = new Texture2D(1, 16);
        hueTexture.wrapMode = TextureWrapMode.Clamp;
        hueTexture.name = "HueTexture";

        // Fill the texture with HSV gradient colors
        for (int i = 0; i < hueTexture.height; ++i)
        {
            hueTexture.SetPixel(0, i, Color.HSVToRGB((float)i / hueTexture.height, 1, 1f));
        }

        // Set the hue image texture
        hueTexture.Apply();
        hueImage.texture = hueTexture;
        currentHue = 0;
        UpdateColorPicker(); 
    }

    private void UpdateColorPicker()
    {
        Vector3 pos = colorPickerObject.GetComponent<RectTransform>().anchoredPosition;
        // float S
        float S;
        float V; 
        if (pos.x <= 0)
        {
            S = 0.5f - (Mathf.Abs(pos.x) / colorPanelWidth); 
        }
        else
        {
            S = 0.5f + (pos.x / colorPanelWidth); 
        }

        // float V
        if (pos.y <= 0)
        {
            V = 0.5f - ( Mathf.Abs(pos.y) / colorPanelHeight);
        }
        else
        {
            V = 0.5f + (pos.y / colorPanelHeight); 
        }

        Color newColor = Color.HSVToRGB(currentHue, S, V);
        colorPickerImage.color = newColor;
        UpdateSphereColor(newColor);

    }
    private void UpdateSphereColor(Color newColor)
    {
        sphereRenderer.material.color = newColor;
    }


    public void UpdateHue(float hue)
    {
        float width = colorPanelTexture.width;
        float height = colorPanelTexture.height;
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                Color newColor = Color.HSVToRGB(hue, (float) i / width, (float) j / height);
                colorPanelTexture.SetPixel(i, j, newColor);
            }
        }

        colorPanelTexture.Apply();
        colorPanelImage.texture = colorPanelTexture;
        currentHue = hue;
        UpdateColorPicker(); 
    }
}
