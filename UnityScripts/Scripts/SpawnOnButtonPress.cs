using System.Collections;
using System.Collections.Generic;
using UnityEngine.InputSystem;
using UnityEngine;

public class SpawnOnButtonPress : MonoBehaviour
{
    public Transform head; 
    private float spawnDistance = 2.0f;
    private float spawnYAxisOffset = 0.25f;
    [SerializeField] InputActionProperty spawnButton;

    private void Update()
    {
        if (spawnButton.action.WasPressedThisFrame())
        {
            transform.position = head.position + new Vector3(head.forward.x, spawnYAxisOffset, head.forward.z).normalized * spawnDistance;
            gameObject.SetActive(!gameObject.activeSelf);
        }
    }
}
