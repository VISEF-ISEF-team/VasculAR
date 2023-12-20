using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
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

    private RectTransform colorPanelTransform;
    private RawImage colorPanelImage;
    private Texture2D colorPanelTexture;
    private Texture2D hueTexture;
    private Image colorPickerImage; 

    private float currentHue;
    private float currentSat;
    private float currentVal;

    private float panelWidth;
    private float panelHeight; 

    private void Start()
    {
        colorPanelImage = colorPanelObject.GetComponent<RawImage>();
        colorPickerImage = colorPickerObject.GetComponent<Image>(); 
        CreateHueImage(); 
        GenerateTexture();

        colorPanelTransform = colorPanelObject.GetComponent<RectTransform>(); 

        panelWidth = colorPanelTransform.rect.width; 
        panelHeight = colorPanelTransform.rect.height;
    }

    private void Update()
    {
        UpdateColorPicker();
        if (leftRayInteractor.IsOverUIGameObject())
        {
            leftRayInteractor.TryGetCurrentUIRaycastResult(out RaycastResult raycastResult, out int raycastEndpointIndex);

        }

        if (rightRayInteractor.IsOverUIGameObject())
        {
            rightRayInteractor.TryGetCurrentUIRaycastResult(out RaycastResult raycastResult, out int raycastEndpointIndex);

        }
    }

    private void GenerateTexture()
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

    private void UpdateColorPicker()
    {
        Vector3 colorPickerPosition = colorPickerObject.transform.position;
        float yNormalized = colorPickerPosition.y / panelHeight;
        float xNormalized = colorPickerPosition.x / panelWidth;
        float currentHue = hueTexture.GetPixel(0, Mathf.RoundToInt(yNormalized * (hueTexture.height - 1))).r; 
      
        colorPickerImage.color = Color.HSVToRGB(currentHue, xNormalized, yNormalized);
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

        hueTexture.Apply();

        // Set the hue image texture
        hueImage.texture = hueTexture;
        currentHue = 0;
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
    }
}
