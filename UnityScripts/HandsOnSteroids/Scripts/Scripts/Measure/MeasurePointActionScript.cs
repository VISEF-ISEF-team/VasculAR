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
    private XRGrabInteractable endSphereGrabbable; 

    private Vector3 originalStartSpherePosition; 
    private Vector3 originalEndSpherePosition; 

    private void Start()
    {
        lineRenderer = GetComponent<LineRenderer>(); 
        distanceText = endSphere.GetComponent<TextMeshProUGUI>();  

        originalStartSpherePosition = transform.position; 
        originalEndSpherePosition = endSphere.transform.position;  

        selfGrabbable = GetComponent<XRGrabInteractable>(); 
        endSphereGrabbable = endSphere.GetComponent<XRGrabInteractable>(); 

        selfGrabbable.selectEntered.AddListener(OnSelfSelectEnter); 
        selfGrabbable.selectExited.AddListener(OnSelfSelectExit); 

        endSphereGrabbable.selectEntered.AddListener(OnEndSphereSelectEnter); 
        endSphereGrabbable.selectExited.AddListener(OnEndSphereSelectExit);
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

    private void OnSelfSelectEnter(SelectEnteredEventArgs args0) 
    {
        Vector3 newPosition = transform.position; 
        if (newPosition != originalStartSpherePosition) 
        {
            originalStartSpherePosition = newPosition; 
            SetDistanceText(); 
        }
    }

    private void OnSelfSelectExit(SelectExitedEventArgs args0) 
    {
        originalStartSpherePosition = transform.position; 
    }

    private void OnEndSphereSelectEnter(SelectEnteredEventArgs args0) 
    {
        Vector3 newPosition = transform.position; 
        if (newPosition != originalEndSpherePosition) 
        {
            originalEndSpherePosition = newPosition; 
            SetDistanceText(); 
        }
    }

    private void OnEndSphereSelectExit(SelectExitedEventArgs args0) 
    {
        originalEndSpherePosition = transform.position; 
    }
}
