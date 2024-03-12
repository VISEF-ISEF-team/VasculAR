from vedo import *
s = Sphere(res=50).linewidth(1)
origins = [[-0.7, 0, 0], [0, -0.6, 0]]
normals = [[-1, 0, 0], [0, -1, 0]]
s.cut_closed_surface(origins, normals)
show(s, axes=1).close()