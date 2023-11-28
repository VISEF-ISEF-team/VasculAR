using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ResetPositionOnFallout : MonoBehaviour
{
    [SerializeField] Transform spawnPosition; 
    private void OnTriggerEnter(Collider other)
    {
        other.transform.position = spawnPosition.position; 
    }
}
