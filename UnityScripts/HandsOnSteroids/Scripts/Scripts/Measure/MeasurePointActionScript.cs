using TMPro;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class MeasurePointActionScript : MonoBehaviour
{
    public GameObject endSphere;
    private LineRenderer lineRenderer;
    private TextMeshProUGUI distanceText;

    // code logic for both when start sphere is moving or end sphere is moving
    private XRGrabInteractable selfGrabbable;
    private XRGrabInteractable endSphereInteractable; 

    private void Start()
    {
        lineRenderer = GetComponent<LineRenderer>(); 
        distanceText = endSphere.GetComponent<TextMeshProUGUI>();   
    }

    public void InitializeStartingSphere()
    {
        if (lineRenderer == null)
        {
            lineRenderer.positionCount++;
            lineRenderer.SetPosition(0, transform.position); 
        }
    }
    public void SetLineRendererPosition(int index, Vector3 position)
    {
        if (lineRenderer != null) 
        {
            if (lineRenderer.positionCount < 2) lineRenderer.positionCount++; 
            lineRenderer.SetPosition(index, position);  
        }
    }
    public float GetDistance()
    {
        float distance = Vector3.Distance(transform.position, endSphere.transform.position);
        return distance; 
    }

    public void SetDistanceText()
    {
        if (distanceText != null) 
        {
            distanceText.text = $"{GetDistance()} cm"; 
        }
    }
}
