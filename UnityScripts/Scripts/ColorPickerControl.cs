using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro; 

public class ColorPickerControl : MonoBehaviour
{
    public float currentHue, currentSat, currentVal;

    [SerializeField] private RawImage hueImage, satValImage, outputImage;
    [SerializeField] private Slider hueSlider;
    [SerializeField] private TMP_InputField hexInputField;

    private Texture2D hueTexture, svTexture, outputTexture;

    [SerializeField] MeshRenderer changeThisColor;

    private void Start()
    {
        // Initialize the color picker components and textures
        CreateHueImage(); 

        CreateSVImage();

        CreateOutputImage();

        UpdateOutputImage();
    }
    private void CreateHueImage()
    {
        // Create a 1x16 texture for the hue gradient
        hueTexture = new Texture2D(1, 16); 
        hueTexture.wrapMode = TextureWrapMode.Clamp;
        hueTexture.name = "HueTexture";

        // Fill the texture with HSV gradient colors
        for (int i =  0; i < hueTexture.height; ++i)
        {
            hueTexture.SetPixel(0, i, Color.HSVToRGB((float) i / hueTexture.height, 1, 0.05f)); 
        }

        hueTexture.Apply();
        currentHue = 0;

        // Set the hue image texture
        hueImage.texture = hueTexture; 
    }

    private void CreateSVImage()
    {
        // Create a 16x16 texture for the saturation and value gradient
        svTexture = new Texture2D(16, 16); 
        svTexture.wrapMode= TextureWrapMode.Clamp;
        svTexture.name = "SatValTexture";

        // Fill the texture with HSV gradient colors based on the current hue
        for (int y = 0; y < svTexture.height; ++y)
        {
            for (int x = 0; x < svTexture.width; ++x)
            {
                svTexture.SetPixel(x, y, Color.HSVToRGB(currentHue, (float)x / svTexture.width, (float)y / svTexture.height)); 

            }
        }

        svTexture.Apply();
        currentSat = 0; 
        currentVal = 0;

        // Set the saturation-value image texture
        satValImage.texture = svTexture; 
    }

    private void CreateOutputImage()
    {
        // Create a 1x16 texture for the output color
        outputTexture = new Texture2D(1, 16); 
        outputTexture.wrapMode = TextureWrapMode.Clamp;
        outputTexture.name = "OutputTexture";

        // Initialize the output texture with the current color
        Color currentColor = Color.HSVToRGB(currentHue, currentSat, currentVal); 

        for (int i = 0; i < outputTexture.height; ++i)
        {
            outputTexture.SetPixel(0, i, currentColor); 
        }

        outputTexture.Apply();
        
        // Set the output image texture
        outputImage.texture = outputTexture;
    }

    private void UpdateOutputImage()
    {
        // Update the output texture with the current color
        Color currentColor = Color.HSVToRGB(currentHue, currentSat, currentVal); 
        for (int i = 0; i < outputTexture.height;  i++)
        {
            outputTexture.SetPixel(0, i, currentColor); 
        }

        outputTexture.Apply();

        hexInputField.text = ColorUtility.ToHtmlStringRGB(currentColor);    

        // Update the color of a specified MeshRenderer
        changeThisColor.material.SetColor("_BaseColor", currentColor); 
    }

    public void SetSV(float s, float v)
    {
        currentSat = s; 
        currentVal = v; 

        UpdateOutputImage();
    }

    public void UpdateSVImage()
    {
        currentHue = hueSlider.value; 

        for (int y = 0; y < outputTexture.height; y++)
        {
            for (int x = 0; x < outputTexture.width; x++)
            {
                svTexture.SetPixel(x, y, Color.HSVToRGB(currentHue, (float) x / svTexture.width, (float) y / svTexture.height));
            }
        }

        svTexture.Apply();

        UpdateOutputImage(); 
    }


    public void OnTextInput()
    {
        if (hexInputField.text.Length < 6)
        {
            return; 
        }

        Color newColor; 

        if (ColorUtility.TryParseHtmlString('#' + hexInputField.text, out newColor))
        {
            Color.RGBToHSV(newColor, out currentHue, out currentSat, out currentVal);

        }
        hueSlider.value = currentHue;
        hexInputField.text = "";
        UpdateOutputImage(); 
    }
}
