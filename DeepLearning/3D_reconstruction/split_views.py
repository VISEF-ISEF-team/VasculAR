from vedo import *

# Create two different scenes
cone = Cone(height=4)
sphere = Sphere()

# Split the rendering window into two views
show(cone, viewup="z", at=0, interactive=False)
show(sphere, viewup="x", at=1, interactive=True)

# Run the rendering loop
show()
