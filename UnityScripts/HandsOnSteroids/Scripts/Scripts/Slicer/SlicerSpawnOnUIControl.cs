using UnityEngine;

public class SlicerSpawnOnUIControl : MonoBehaviour
{
    public Transform head;
    public GameObject planeObject;
    private float spawnDistance = 2.0f;
    private float spawnYAxisOffset = 0.25f;
    public void SpawnSlicer()
    {
        transform.position = head.position + new Vector3(head.forward.x, spawnYAxisOffset, head.forward.z).normalized * spawnDistance;
    }
}
