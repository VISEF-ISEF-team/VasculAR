import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, measure

path = "C:/Users/Admin/Pictures/Screenshots/Screenshot 2023-12-18 201458.png"
image = io.imread(path, as_gray=True)
threshold_value = 0.5  
binary_image = image > threshold_value
contours = measure.find_contours(binary_image, 0.8)  
fig, ax = plt.subplots()
ax.imshow(image, cmap=plt.cm.gray)

for contour in contours:
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2, color='red')

print(contours)

ax.axis('image')
plt.title("Khoanh viền cung động mạch chủ đôi")
plt.show()