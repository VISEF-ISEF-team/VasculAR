using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ColorPickerControllerScript : MonoBehaviour
{
    [SerializeField] GameObject colorPanelObject;
    [SerializeField] MeshRenderer sphereRenderer; 
    private RectTransform colorPanelTransform;
    private RawImage colorPanelImage; 
    private Texture2D colorPanelTexture;

    private void Start()
    {
        colorPanelImage = colorPanelObject.GetComponent<RawImage>();

        GenerateTexture();
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
                Color newColor = Color.HSVToRGB(1, (float) i / width, (float) j / height);  
                colorPanelTexture.SetPixel(i, j, newColor);
            }
        }

        colorPanelTexture.Apply();

        colorPanelImage.texture = colorPanelTexture;
    }

    public void UpdateTexture(float hue)
    {
        float width = colorPanelTexture.width;
        float height = colorPanelTexture.height;
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
    }


}
