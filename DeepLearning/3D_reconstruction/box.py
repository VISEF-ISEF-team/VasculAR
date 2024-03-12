from vedo import *


# Define the dimensions of the bounding box
length = 10
width = 5
height = 3

# Create the bounding box
bbox = Box(pos=(0, 0, 0), length=length, width=width, height=height, alpha=0.3)

p = Plane(
	pos=(5, 0, 0),
	normal=(0, 0, 1),
	s=(1, 1),
	res=(1, 1),
	c='gray5',
	alpha=1.0
)

# Show the bounding box
bbox.show()
p.show()
