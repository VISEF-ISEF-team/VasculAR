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
        set { if (value.x > 0&& value.y > 0 && value.z > 0) realSphereSize = value; }
    }
    private void Start()
    {
        handPositions = GetHandPosition.GetHandPositionReference(); 
    }
    private void Update()
    {
        if (allowLeftHand)
        {
            if (lefttriggerButton.action.WasPressedThisFrame())
            {
                DrawParticles(true);
            }
        }
        else
        {
            if (righttriggerButton.action.WasPressedThisFrame())

                DrawParticles(false);
        }
    }
    private void DrawParticles(bool allowLeftHandArgs)
    {
        Transform leftHandTip = handPositions.GetHandTipPositions()[0]; 
        Transform rightHandTip = handPositions.GetHandTipPositions()[1];
        Color otherSphereColor = otherSphereMeshRenderer.material.color;
        spherePrefab.GetComponent<MeshRenderer>().material.SetColor("New Color", otherSphereColor);
        spherePrefab.transform.localScale = realSphereSize; 
        if (allowLeftHandArgs)
        {
            Instantiate(spherePrefab, new Vector3(leftHandTip.position.x + xOffset, leftHandTip.position.y, leftHandTip.position.z), Quaternion.identity);
        }
        else
        {
            Instantiate(spherePrefab, new Vector3(rightHandTip.position.x + xOffset, rightHandTip.position.y, rightHandTip.position.z), Quaternion.identity);
        }
    }
}
