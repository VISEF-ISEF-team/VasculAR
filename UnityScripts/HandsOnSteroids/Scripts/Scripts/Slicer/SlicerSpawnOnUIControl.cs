using UnityEngine;

public class SlicerSpawnOnUIControl : MonoBehaviour
{
    public Transform head;
    private float spawnDistance = 2.0f;
    private float spawnYAxisOffset = -0.1f;
    public void SpawnSlicer()
    {
        transform.position = head.position + new Vector3(head.forward.x, spawnYAxisOffset, head.forward.z).normalized * spawnDistance;
    }
}
