using UnityEngine;
using UnityEngine.UI;

public class SegmentButtonActionScript : MonoBehaviour
{
    public int segmentNumber;
    public Mesh mesh;
    public Vector3[] originalVerticies;
    private bool isPressed = false;
    private Button button;
    private Color pressedColor;
    private ColorBlock originalColors;

    private void Start()
    {
        button = GetComponent<Button>();
        originalColors = button.colors;
        pressedColor = originalColors.pressedColor;
        button.onClick.AddListener(OnMeshButtonClick);

    }

    private void OnMeshButtonClick()
    {
        isPressed = !isPressed;
        if (isPressed)
        {
            if (segmentNumber < mesh.subMeshCount)
            {
                int[] triangles = mesh.GetTriangles(segmentNumber);
                Vector3[] vertices = mesh.vertices;

                foreach (int triIndex in triangles)
                {
                    vertices[triIndex] = new Vector3(float.MaxValue, float.MaxValue, float.MaxValue);
                }
                mesh.vertices = vertices;
            }
            ColorBlock newColors = button.colors;
            newColors.normalColor = pressedColor;
            button.colors = newColors;
        }
        else
        {
            if (segmentNumber < mesh.subMeshCount)
            {
                int[] triangles = mesh.GetTriangles(segmentNumber);
                Vector3[] vertices = mesh.vertices;

                foreach (int triangleIndex in triangles)
                {
                    vertices[triangleIndex] = originalVerticies[triangleIndex];
                }

                mesh.vertices = vertices;
            }
            button.colors = originalColors;
        }
    }
}
