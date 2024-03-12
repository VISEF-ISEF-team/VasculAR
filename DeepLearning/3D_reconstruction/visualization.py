import vedo
from vedo import load, show, Text2D

mesh = load('coronary.stl')

# Calculate the volume of the mesh
volume = mesh.volume()

# Calculate the surface area of the mesh
area = mesh.area()

# Create Text2D objects for volume and area
volume_text = Text2D(f"Volume: {volume:.2f}", pos=(0.1, 0.9), s=0.03, c="black")
area_text = Text2D(f"Surface Area: {area:.2f}", pos=(0.1, 0.85), s=0.03, c="black")

print(volume, area)

# Show the mesh and the text
show(mesh, volume_text, area_text, interactive=True)


