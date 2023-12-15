using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class DeleteSliceOnButtonPress : MonoBehaviour
{
    [SerializeField] InputActionProperty deleteButton;
    private void Update()
    {
        if (deleteButton.action.WasPressedThisFrame())
        {
            Destroy(gameObject);
        }
    }

}
