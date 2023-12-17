using UnityEngine;
using EzySlice;
using UnityEngine.InputSystem; 

public class EnableSlice : MonoBehaviour
{
    public EnableSlice baseEnableSlice;
    private DeleteSliceOnButtonPress baseDeleteSliceOnButtonPress;

    public GameObject heartTarget;
    public Material crossSectionMaterial;

    public Transform planeCoordinates;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Slice(heartTarget); 
        }
    }

    // normal of a plane is a vector that is perpendicular to the plane
    public void Slice(GameObject target)
    {
        SlicedHull hull = target.Slice(planeCoordinates.position, planeCoordinates.up);
        Debug.Log(target.name); 

        if (hull != null)
        {
            // upper hull
            GameObject upperHull = hull.CreateUpperHull(target, crossSectionMaterial);
            SliceComponentSetup(upperHull, true, target.name);
            upperHull.transform.position = new Vector3(heartTarget.transform.position.x + 1.5f, heartTarget.transform.position.y, heartTarget.transform.position.z);

            // lower hull
            GameObject lowerHull = hull.CreateLowerHull(target, crossSectionMaterial);
            SliceComponentSetup(lowerHull, false, target.name);
            lowerHull.transform.position = new Vector3(heartTarget.transform.position.x - 1.5f, heartTarget.transform.position.y, heartTarget.transform.position.z);
        }
    }

    public void SliceComponentSetup(GameObject sliceComponent, bool upper, string baseName)
    {
        // set delete on slice
/*        DeleteSliceOnButtonPress currentDeleteSliceOnButtonPressSettings = sliceComponent.AddComponent<DeleteSliceOnButtonPress>();*/

        // set enable slice 
        EnableSlice currentEnableSlice = sliceComponent.AddComponent<EnableSlice>();

        currentEnableSlice.heartTarget = sliceComponent;

        currentEnableSlice.crossSectionMaterial = baseEnableSlice.crossSectionMaterial;

        currentEnableSlice.planeCoordinates = baseEnableSlice.planeCoordinates;

        currentEnableSlice.baseEnableSlice = baseEnableSlice; 

        // set name for sliced component
        if (upper)
        {
            sliceComponent.name = $"{baseName}-upper";
        }
        else
        {
            sliceComponent.name = $"{baseName}-lower";
        }
    }
}
