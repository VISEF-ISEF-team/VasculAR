using TMPro;
using System; 
using UnityEngine;

public class MeasreSphereScript : MonoBehaviour
{
    public GameObject endSphere;

    private LineRenderer lineRenderer;

    private TextMeshProUGUI startDistanceText; 
    private TextMeshProUGUI endDistanceText;

    private Vector3 originalStartSpherePosition;
    private Vector3 originalEndSpherePosition;

    private float offset = 0.05f;

    private bool selfIsGrabbed = true; 
    private bool endSphereGrabbed = false;
    private void Start()
    {
        startDistanceText = GetComponentInChildren<TextMeshProUGUI>();
        endDistanceText = endSphere.GetComponentInChildren<TextMeshProUGUI>();

        originalStartSpherePosition = transform.position;
        originalEndSpherePosition = endSphere.transform.position; 

        lineRenderer = GetComponent<LineRenderer>();

        InitializeStartingSphere();
        SetDistanceText(); 
    }
    private void Update()
    {
        if (transform.position != originalStartSpherePosition)
        {
            originalStartSpherePosition = transform.position;
            SetLineRendererPosition(0, originalStartSpherePosition);
            SetDistanceText(); 
        }
        if (endSphere.transform.position != originalEndSpherePosition)
        {
            originalEndSpherePosition = endSphere.transform.position;
            SetLineRendererPosition(1, originalEndSpherePosition);
            SetDistanceText(); 
        }
/*        if (selfIsGrabbed)
        {
            Vector3 mousePosition = GetMousePosition(); 
            if (mousePosition != originalStartSpherePosition)
            {
                originalStartSpherePosition = mousePosition;
*//*                transform.position = mousePosition;*//*
                SetLineRendererPosition(0, mousePosition); 
                SetDistanceText(); 
            }
        }*/
/*        else if (endSphereGrabbed)
        {
            Vector3 mousePosition = GetMousePosition();
            if (mousePosition != originalEndSpherePosition)
            {
                originalEndSpherePosition = mousePosition;
                endSphere.transform.position = mousePosition;
                SetLineRendererPosition(1, mousePosition); 
                SetDistanceText();
            }
        }*/
        Debug.Log($"{selfIsGrabbed}, {endSphereGrabbed}"); 
    }

    private void OnMouseDown()
    {
        Vector3 pos = GetMousePosition(); 
        if (Vector3.Distance(pos, gameObject.transform.position) < offset)
        {
            selfIsGrabbed = true;
            endSphereGrabbed = false; 
        }
        else if (Vector3.Distance(pos, endSphere.transform.position) < offset)
        {
            endSphereGrabbed = true;
            selfIsGrabbed = false; 
        }
        Debug.Log("Mouse Down"); 
    }
    private void OnMouseUp()
    {
        if (selfIsGrabbed) selfIsGrabbed = false;
        if (endSphereGrabbed) endSphereGrabbed = false;

        Debug.Log("Mouse Up"); 
    }
    private Vector3 GetMousePosition()
    {
        // Get the mouse position in screen coordinates
        Vector3 mouseScreenPos = Input.mousePosition;

        // Set the z-coordinate to the camera's near clip plane
        mouseScreenPos.z = Camera.main.nearClipPlane;

        // Convert the mouse position to world coordinates
        Vector3 mouseWorldPos = Camera.main.ScreenToWorldPoint(mouseScreenPos);

        // Output the mouse position in world coordinates
        return mouseWorldPos;   
    }
    public float GetDistance()
    {
        float distance = Vector3.Distance(transform.position, endSphere.transform.position);
        distance = (float)Math.Round(distance, 2); 
        return distance;
    }

    public void SetDistanceText()
    {
        if (endDistanceText != null)
        {
            endDistanceText.text = $"{GetDistance()} cm";
        }
        if (startDistanceText != null)
        {
            startDistanceText.text = $"{GetDistance()} cm";
        }
    }
    private void InitializeStartingSphere()
    {
        if (lineRenderer != null)
        {
            lineRenderer.positionCount++;
            lineRenderer.SetPosition(0, transform.position);
            lineRenderer.positionCount++; 
            lineRenderer.SetPosition(1, endSphere.transform.position); 
        }
    }
    public void SetLineRendererPosition(int index, Vector3 position)
    {
        if (lineRenderer != null)
        {
            lineRenderer.SetPosition(index, position);
        }
    }
}
