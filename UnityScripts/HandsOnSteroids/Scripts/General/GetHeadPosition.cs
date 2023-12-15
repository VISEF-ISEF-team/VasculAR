using UnityEngine;

public class GetHeadPosition : MonoBehaviour
{
    private float spawnDistance = 2.0f;
    public float SpawnDistance
    {
        get { return spawnDistance; }
        set
        {
            if (IsNumber(value))
            {
                spawnDistance = value;
            }
        }
    }
    [SerializeField] Transform headConfigObjectTransform; 
    public Vector3 TransformPositionInFrontOfHead()
    {
        return headConfigObjectTransform.position + new Vector3(headConfigObjectTransform.forward.x, 0, headConfigObjectTransform.forward.z).normalized * spawnDistance;
    }

    public Vector3 TransformToLookAt(float objectPosition)
    {
        Vector3 lookAtCoordinates = new Vector3();
        {
            lookAtCoordinates.x = headConfigObjectTransform.position.x;
            lookAtCoordinates.y = objectPosition; 
            lookAtCoordinates.z = headConfigObjectTransform.position.z;
        }
        return lookAtCoordinates;   
    }
    private bool IsNumber(object variable)
    {
        // Check if the variable is a number
        return variable is int || variable is float || variable is double || variable is decimal;
    }

    public static GetHeadPosition GetHeadPositionReference()
    {
       GetHeadPosition component = GameObject.Find("General Settings").GetComponent<GetHeadPosition>();
        return component; 
    }
}
