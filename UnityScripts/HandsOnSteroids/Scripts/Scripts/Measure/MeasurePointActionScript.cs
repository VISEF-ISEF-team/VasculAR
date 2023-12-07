using TMPro;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using System; 

public class MeasurePointActionScript : MonoBehaviour
{
    public GameObject endSphere;
    private LineRenderer lineRenderer;
    private TextMeshProUGUI endDistanceText;
    private TextMeshProUGUI startDistanceText; 

    // code logic for both when start sphere is moving or end sphere is moving
    private XRGrabInteractable selfGrabbable;
    private XRGrabInteractable endSphereGrabbable;

    private Vector3 originalStartSpherePosition;
    private Vector3 originalEndSpherePosition;

    private bool allowDelete = false;
    public bool AllowDelete
    {
        get { return allowDelete; }
        set { allowDelete = value; }
    }

    private bool allowGrab = false; 
    public bool AllowGrab
    {
        get { return allowGrab; }
        set { allowGrab = value; }
    }

    private void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();
        startDistanceText = GetComponentInChildren<TextMeshProUGUI>();
        endDistanceText = endSphere.GetComponentInChildren<TextMeshProUGUI>();

        originalStartSpherePosition = transform.position;
        originalEndSpherePosition = endSphere.transform.position;

        if (allowGrab)
        {
            selfGrabbable = GetComponent<XRGrabInteractable>();
            endSphereGrabbable = endSphere.GetComponent<XRGrabInteractable>();

            selfGrabbable.selectEntered.AddListener(OnSelfSelectEnter);
            selfGrabbable.selectExited.AddListener(OnSelfSelectExit);
            selfGrabbable.activated.AddListener(OnSelfActivate);
            // selfGrabbable.deactivated.AddListener(OnSelfDeactivate); 

            endSphereGrabbable.selectEntered.AddListener(OnEndSphereSelectEnter);
            endSphereGrabbable.selectExited.AddListener(OnEndSphereSelectExit);
            endSphereGrabbable.activated.AddListener(OnEndSphereActivate);
            // endSphereGrabbable.deactivated.AddListener(OnEndSphereDeactivate); 
        }
    }

    public void InitializeStartingSphere()
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
            if (lineRenderer.positionCount < 2) lineRenderer.positionCount++;
            lineRenderer.SetPosition(index, position);
        }
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

    private void OnSelfSelectEnter(SelectEnterEventArgs args0)
    {
        Vector3 newPosition = transform.position;
        if (newPosition != originalStartSpherePosition)
        {
            originalStartSpherePosition = newPosition;
            SetDistanceText();
            SetLineRendererPosition(0, newPosition); 
        }
    }

    private void OnSelfSelectExit(SelectExitEventArgs args0)
    {
        originalStartSpherePosition = transform.position;
    }

    private void OnSelfActivate(ActivateEventArgs args0)
    {
        if (allowDelete)
        {
            Destroy(endSphere);
            Destroy(gameObject);
        }
    }

    private void OnEndSphereSelectEnter(SelectEnterEventArgs args0)
    {
        Vector3 newPosition = transform.position;
        if (newPosition != originalEndSpherePosition)
        {
            originalEndSpherePosition = newPosition;
            SetDistanceText();
            SetLineRendererPosition(1, newPosition); 
        }
    }

    private void OnEndSphereSelectExit(SelectExitEventArgs args0)
    {
        originalEndSpherePosition = transform.position;
    }

    private void OnEndSphereActivate(ActivateEventArgs args0)
    {
        if (allowDelete)
        {
            Destroy(endSphere);
            Destroy(gameObject);
        }
    }
}