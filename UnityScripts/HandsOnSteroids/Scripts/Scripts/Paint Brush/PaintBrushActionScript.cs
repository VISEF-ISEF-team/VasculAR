using UnityEngine;
using UnityEngine.InputSystem; 
public class PaintBrushActionScript : MonoBehaviour
{
    [SerializeField] GameObject spherePrefab;
    [SerializeField] public MeshRenderer otherSphereMeshRenderer;
    [SerializeField] InputActionProperty righttriggerButton;
    [SerializeField] InputActionProperty lefttriggerButton;
    private GetHandPosition handPositions;
    private readonly float xOffset = 0.05f;
    private bool allowLeftHand; 
    public bool AllowLeftHand
    {
        get { return allowLeftHand; }
        set { if (allowLeftHand != value) allowLeftHand = value; }
    }
    private Vector3 realSphereSize; 
    public Vector3 RealSphereSize
    {
        get { return realSphereSize; }
        set { realSphereSize = value; }
    }

    public bool allowDrawing = false; 
    private void Start()
    {
        handPositions = GetHandPosition.GetHandPositionReference(); 
    }
    private void Update()
    {
        if (allowDrawing)
        {
            if (allowLeftHand)
            {
                if (lefttriggerButton.action.ReadValue<float>() > 0.5f)
                {
                    DrawParticles(true);
                }
                else if (righttriggerButton.action.ReadValue<float>() > 0.5f)
                {
                    DrawParticles(false); 
                }
            }
            else
            {
                if (righttriggerButton.action.ReadValue<float>() > 0.5f)

                    DrawParticles(false);
            }
        }
    }
    private void DrawParticles(bool leftHand)
    {
        Transform leftHandTip = handPositions.GetHandTipPositions()[0]; 
        Transform rightHandTip = handPositions.GetHandTipPositions()[1];

        // the color will be update continously whenever color picker is changed since when color picker's color changes, the otherSphereMeshRenderer is changed as well
        Color otherSphereColor = otherSphereMeshRenderer.material.color;
        if (leftHand)
        {
            GameObject paintSphere = Instantiate(spherePrefab, new Vector3(leftHandTip.position.x + xOffset, leftHandTip.position.y, leftHandTip.position.z), Quaternion.identity);
            paintSphere.transform.localScale = realSphereSize;
            paintSphere.GetComponent<MeshRenderer>().material.color = otherSphereColor; 
        }
        else
        {
            GameObject paintSphere = Instantiate(spherePrefab, new Vector3(rightHandTip.position.x + xOffset, rightHandTip.position.y, rightHandTip.position.z), Quaternion.identity);
            paintSphere.transform.localScale = realSphereSize;
            paintSphere.GetComponent<MeshRenderer>().material.color = otherSphereColor; 
        }
    }
}
