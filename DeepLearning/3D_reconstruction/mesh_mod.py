"""Modify mesh vertex positions"""
from vedo import *

mesh = Sphere()

points = mesh.points()
faces = mesh.faces()
neighborhood_map = {}

for vertex_index in range(len(points)):
    neighbor_points = set()
    
    for face in faces:
        if vertex_index in face:
            neighbor_points.update(face)
            face_index = faces.index(face)
            for i in range(face_index, face_index+51, 1):
                if (i >= len(faces)):
                    break
                neighbor_points.update(faces[i])
            break
                
    neighborhood_map[vertex_index] = list(neighbor_points)
    
print("Neighborhood points for vertex 10:", neighborhood_map[10], len(neighborhood_map[10]))

        
plt = Plotter(interactive=False, axes=1)
plt.show(mesh)

def distort(index, new):
    distorted_points = mesh.points 
    vel=0.4
    for idx_vert in neighborhood_map[index]:
        mesh.points[idx_vert] += (np.array([vel,vel,vel]) * np.array(new)).tolist()
        vel -= 0.0025
            
    distorted_mesh = Mesh([distorted_points, mesh.faces])

    plt.clear()
    plt.show(distorted_mesh)
    plt.reset_camera().render()
    

closest_idx = None

def func(evt):
    picked = evt.picked3d
    global closest_idx
    if picked is not None:
        closest_idx = mesh.closest_point(picked, return_point_id=True)
        
change = 2
def func2(evt):
    global closest_idx, change
    key_pressed = evt.keypress
    if closest_idx != None:
        if (key_pressed == 't'):
            distort(closest_idx, [0,1,0])
        if (key_pressed == 'r'):
            distort(closest_idx, [1,1,0])
        if (key_pressed == 'f'):
            distort(closest_idx, [1,0,0])
        if (key_pressed == 'v'):
            distort(closest_idx, [-1,-1,0])
        if (key_pressed == 'b'):
            distort(closest_idx, [0,-1,0])
        if (key_pressed == 'n'):
            distort(closest_idx, [0,-1,-1])
        if (key_pressed == 'h'):
            distort(closest_idx, [-1,0,0])
        if (key_pressed == 'y'):
            distort(closest_idx, [1,1,0])
        if (key_pressed == 'g'):
            closest_idx=None
            

plt.add_callback('LeftButtonClick', func)
plt.add_callback('KeyPress', func2)
plt.interactive().close()
