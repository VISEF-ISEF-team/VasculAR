import numpy as np
from skimage import io, color, morphology
import matplotlib.pyplot as plt

# Load an example binary image (you can use your own binary image)
image_path = 'D:/Documents/GitHub/VascuIAR/GUIApp/temp10.png'
binary_image = io.imread(image_path, as_gray=True)

# Ensure the image is binary (threshold if needed)
binary_image = binary_image > 0.5

# Apply skeletonization
skeletonized_image = morphology.skeletonize(binary_image)

# Plot the original and skeletonized images side by side
fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(binary_image, cmap='gray')
axes[0].set_title('Phân vùng động mạch phổi')

axes[1].imshow(skeletonized_image, cmap='gray')
axes[1].set_title('Cấu trúc hóa động mạch phổi')

plt.show()