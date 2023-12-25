using UnityEngine;
using UnityEngine.UI;

public class SegmentButtonActionScript : MonoBehaviour
{
    // rewrite this file to be suitable for the newly created segmentation 
    public GameObject segmentObjectChild; 
    public string segmentName;
    private bool isPressed = false;
    private Button button;
    private Color pressedColor;
    private ColorBlock originalColors;

    private void Start()
    {
        button = GetComponent<Button>();
        originalColors = button.colors;
        pressedColor = originalColors.pressedColor;
        if (segmentName != null && segmentObjectChild != null )
        {
            button.onClick.AddListener(OnSegmentButtonClick);
        }

    }
    private void OnSegmentButtonClick()
    {
        isPressed = !isPressed;
        if (isPressed)
        {
            segmentObjectChild.SetActive(false); 
            ColorBlock newColors = button.colors;
            newColors.normalColor = pressedColor;
            button.colors = newColors;
        }
        else
        {
            segmentObjectChild.SetActive(true); 
            button.colors = originalColors;
        }
    }
}
