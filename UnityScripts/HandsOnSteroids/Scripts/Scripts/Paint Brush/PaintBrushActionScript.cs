using UnityEngine;
using UnityEngine.InputSystem; 
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit; 
public class PaintBrushActionScript : MonoBehaviour
{
    [SerializeField] GameObject spherePrefab;
    [SerializeField] public MeshRenderer otherSphereMeshRenderer;
    [SerializeField] InputActionProperty righttriggerButton;
    [SerializeField] InputActionProperty lefttriggerButton;
    private GetHandPosition handPositions;
    private float xOffset = 0.05; 
    public bool allowLeftHand = false;

    private void Start()
    {
        handPositions = ScriptableObject.CreateInstance<GetHandPosition>();
        handPositions.StartScript(); 
    }
    private void Update()
    {
        if (allowLeftHand)
        {
            if (lefttriggerButton.action.WasPressedThisFrame())
            {
                DrawParticles(true); 
            }
            else
            {
                DrawParticles(false); 
            }
        }
        
    }

    private void DrawParticles(bool allowLeftHandArgs)
    {
        Transform leftHandTip = handPositions.GetHandTipPositions()[0]; 
        Transform rightHandTip = handPositions.GetHandTipPositions()[1];
        Color otherSphereColor = otherSphereMeshRenderer.material.color;
        spherePrefab.GetComponent<MeshRenderer>().material.SetColor("New Color", otherSphereColor);
        if (allowLeftHandArgs)
        {
            Instantiate(spherePrefab, Vector3(leftHandTip.position.x + xOffset, leftHandTip.position.y, leftHandTip.position.z), Quaternion.identity);
        }
        else
        {
            Instantiate(spherePrefab, Vector3(rightHandTip.position.x + xOffset, rightHandTip.position.y, rightHandTip.position.z, Quaternion.identity);
        }
    }
}
