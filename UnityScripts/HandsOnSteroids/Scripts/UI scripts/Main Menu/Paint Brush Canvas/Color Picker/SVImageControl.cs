using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.UI;

public class SVImageControl : MonoBehaviour, IDragHandler, IPointerClickHandler
{
    [SerializeField] private Image pickerImage;
    [SerializeField] XRRayInteractor leftRayInteractor;
    [SerializeField] XRRayInteractor rightRayInteractor;

    private RawImage SVImage;

    private ColorPickerControl CC;

    private RectTransform rectTransform, pickerTransform;

    private void Awake()
    {
        SVImage = GetComponent<RawImage>(); 
        CC = FindObjectOfType<ColorPickerControl>();    
        rectTransform = GetComponent<RectTransform>();

        pickerTransform = pickerImage.GetComponent<RectTransform>();
        pickerTransform.position = new Vector2(-(rectTransform.sizeDelta.x * 0.5f), -(rectTransform.sizeDelta.y * 0.5f));

        leftRayInteractor.selectEntered.AddListener(OnLeftRaySelectEnter);
        rightRayInteractor.selectEntered.AddListener(OnRIghtRaySelectEnter);
    }

    private void OnLeftRaySelectEnter(SelectEnterEventArgs arg0)
    {
        leftRayInteractor.TryGetHitInfo(out Vector3 position, out _, out _, out _);
        position = rectTransform.InverseTransformDirection(position);
        pickerTransform.localPosition = position;
        Debug.Log(position); 
    }

    private void OnRIghtRaySelectEnter(SelectEnterEventArgs arg0)
    {
        rightRayInteractor.TryGetHitInfo(out Vector3 position, out _, out _, out _);
        position = rectTransform.InverseTransformDirection(position); 
        pickerTransform.localPosition = position;
        Debug.Log(position); 
    }

    void UpdateColor(PointerEventData eventData)
    {
        Vector3 pos = rectTransform.InverseTransformPoint(eventData.position);

        float deltaX = rectTransform.sizeDelta.x * 0.5f;
        float deltaY = rectTransform.sizeDelta.y * 0.5f;

        if (pos.x < -deltaX)
        {
            pos.x = -deltaX;
        }
        else if (pos.x > deltaX)
        {
            pos.x = deltaX;
        }

        if (pos.y < -deltaY)
        {
            pos.y = -deltaY;
        }
        else if (pos.y > deltaY)
        {
            pos.y = deltaY;
        }

        float x = pos.x + deltaX;
        float y = pos.y + deltaY;

        float xNorm = x / rectTransform.sizeDelta.x;
        float yNorm = y / rectTransform.sizeDelta.y;

        pickerTransform.localPosition = pos;
        pickerImage.color = Color.HSVToRGB(0, 0, 1 - yNorm);

        CC.SetSV(xNorm, yNorm);
    }
    public void OnDrag(PointerEventData eventData)
    {
        UpdateColor(eventData); 
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        UpdateColor(eventData); 
    }
}
