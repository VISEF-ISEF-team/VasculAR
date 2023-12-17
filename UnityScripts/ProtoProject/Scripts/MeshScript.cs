using UnityEngine;

public class MeshScript : MonoBehaviour
{
    private MeshFilter meshFilter;
    private Vector3[] originalVertices;
    private Mesh mesh;
    private int submeshToHide;
    private bool isHiding = false;

    private void Start()
    {
        meshFilter = GetComponentInChildren<MeshFilter>();
        mesh = meshFilter.mesh;
        submeshToHide = 0;
        originalVertices = mesh.vertices.Clone() as Vector3[];
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (isHiding)
            {
                // Restore the original listVertices
                /*mesh.listVertices = originalVertices;*/
                Vector3[] vertices = mesh.vertices;
                int[] triangles = mesh.GetTriangles(submeshToHide);

                foreach (int triangleIndex in triangles)
                {
                    vertices[triangleIndex] = originalVertices[triangleIndex];
                }

                mesh.vertices = vertices;
            }
            else
            {
                // Hide the listVertices (set them to a large value)
                Vector3[] vertices = mesh.vertices;
                int[] triangles = mesh.GetTriangles(submeshToHide);

                foreach (int triangleIndex in triangles)
                {
                    vertices[triangleIndex] = new Vector3(float.MaxValue, float.MaxValue, float.MaxValue);
                }

                mesh.vertices = vertices;
            }

            // Toggle the state
            isHiding = !isHiding;
        }
    }
}
