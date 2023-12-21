using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ColorPickerControllerScript : MonoBehaviour
{
    [SerializeField] GameObject colorPanelObject;
    [SerializeField] MeshRenderer sphereRenderer; 
    [SerializeField] RawImage hueImage;
    [SerializeField] GameObject colorPicker;

    private Image colorPickerImage; 
    private RectTransform colorPanelTransform;
    private RawImage colorPanelImage;
    private Texture2D colorPanelTexture;
    private Texture2D hueTexture; 

    private float currentHue;
    private float colorPanelWidth;
    private float colorPanelHeight;
    private Vector2 centerPoint; 

    private void Start()
    {
        colorPanelImage = colorPanelObject.GetComponent<RawImage>();
        colorPickerImage = colorPicker.GetComponent<Image>();
        colorPanelTransform = colorPanelObject.GetComponent<RectTransform>();

        colorPanelWidth = colorPanelTransform.rect.width;
        colorPanelHeight = colorPanelTransform.rect.height; 

        centerPoint = new Vector2(colorPanelWidth / 2, colorPanelHeight / 2);
        Debug.Log(centerPoint.ToString()); 

        GenerateHueImage();
        GenerateTexture();
        UpdateColorPicker();
    }

    private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            // Get the mouse position in screen coordinates
            Vector3 mousePosition = Input.mousePosition;

            // Optionally, convert the screen coordinates to world coordinates if needed
            /*         mousePosition = Camera.main.ScreenToWorldPoint(mousePosition);*/

/*            mousePosition = colorPanelTransform.InverseTransformPoint(mousePosition);*/
            Debug.Log(mousePosition);
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
                Color newColor = Color.HSVToRGB(currentHue, (float) i / width, (float) j / height);  
                colorPanelTexture.SetPixel(i, j, newColor);
            }
        }

        colorPanelTexture.Apply();
        colorPanelImage.texture = colorPanelTexture;
    }

    private void GenerateHueImage()
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

    public void UpdateTexture(float hue)
    {
        float width = colorPanelTexture.width;
        float height = colorPanelTexture.height;

        colorPanelTexture = new Texture2D( (int) width, (int) height); 
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                Color newColor = Color.HSVToRGB(hue, (float)i / width, (float)j / height);
                colorPanelTexture.SetPixel(i, j, newColor);
            }
        }

        colorPanelTexture.Apply();
        colorPanelImage.texture = colorPanelTexture;
        currentHue = hue;

        UpdateColorPicker(); 
    }

    public void UpdateColorPicker()
    {
        Vector3 pos = colorPicker.transform.position;
        pos = colorPanelTransform.InverseTransformPoint(pos);
        Vector2 newPos = (centerPoint - new Vector2(pos.x, pos.z) );
        newPos.x /= colorPanelWidth;
        newPos.y /= colorPanelWidth;
        Color newColor = Color.HSVToRGB(currentHue, newPos.x, newPos.y);
        colorPickerImage.color = newColor;
        UpdateSphereColor(newColor); 
    }

    private void UpdateSphereColor(Color newColor)
    {
        sphereRenderer.material.color = newColor; 
    }
}
