import numpy as np
from skimage import io, color, morphology
import matplotlib.pyplot as plt

# Load an example binary image (you can use your own binary image)
image_path = "C:/Users/Admin/Pictures/Screenshots/Screenshot 2023-12-18 201458.png"
binary_image = io.imread(image_path, as_gray=True)

# Ensure the image is binary (threshold if needed)
binary_image = binary_image > 0.5

# Apply skeletonization
skeletonized_image = morphology.skeletonize(binary_image)

# Plot the original and skeletonized images side by side
fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(binary_image, cmap='gray')
axes[0].set_title('Cung động mạch chủ')

axes[1].imshow(skeletonized_image, cmap='gray')
axes[1].set_title('Cấu trúc hóa cung động mạch chủ')

plt.show()