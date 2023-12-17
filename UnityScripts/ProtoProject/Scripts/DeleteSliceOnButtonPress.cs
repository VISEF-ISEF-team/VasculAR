using UnityEngine;

public class DeleteSliceOnButtonPress : MonoBehaviour
{
    private bool allowDelete = true; 

    private void Start()
    {

    }

    private void Update()
    {
        if (allowDelete && Input.GetKeyDown(KeyCode.D))
        {
            Destroy(gameObject);
        }
    }
}
