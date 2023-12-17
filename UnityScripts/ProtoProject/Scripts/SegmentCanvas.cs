using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SegmentCanvas : MonoBehaviour
{
    [SerializeField] Image buttonPrefab;
    [SerializeField] GameObject segmentObject;
    [SerializeField] GameObject segmentCanvas;

    private MeshFilter meshFilter;
    private Mesh mesh;
    private Vector3[] originalVertices;

    private int[] submeshIndices; 
    private void Start()
    {
        meshFilter = segmentObject.GetComponentInChildren<MeshFilter>();
        mesh = meshFilter.mesh;
        originalVertices = mesh.vertices.Clone() as Vector3[];

        SetupButton();
    }

    private void Update()
    {
        
    }

    private void SetupButton()
    {
        Transform canvasTransform = segmentCanvas.GetComponent<Transform>();
        int order = 1; 
        for (int i = 0; i < canvasTransform.childCount; ++i)
        {
            GameObject child = canvasTransform.GetChild(i).gameObject;
            TextMeshProUGUI buttonText = child.GetComponentInChildren<TextMeshProUGUI>();
            if (buttonText != null)
            {
                buttonText.text = $"Segment no.{order}";
                order++; 
                SegmentButtonActionScript actionScript = child.AddComponent<SegmentButtonActionScript>();
                actionScript.mesh = mesh;
                actionScript.segmentNumber = order;
                actionScript.originalVerticies = originalVertices; 
            }   
        }
    }
}
