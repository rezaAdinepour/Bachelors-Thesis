import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import local_binary_pattern
from skimage.color import gray2rgb, rgb2gray
from skimage.io import imread

# Load the image
img = imread('reza.jpg')

# Convert the image to grayscale if it is in RGB format
if (img.ndim == 3):
    img = rgb2gray(img)

# Compute the LBP transformation
lbp = local_binary_pattern(img, 8, 1.5)

# Convert the LBP image to a color image for display purposes
lbp_color = gray2rgb(lbp)

# Display the original and LBP transformed images
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

ax1.imshow(img, cmap=plt.cm.gray)
ax1.set_title('Original Image')

ax2.imshow(lbp_color)
ax2.set_title('LBP Transformed Image')

for ax in (ax1, ax2):
    ax.axis('off')

plt.show()

# Plot the pixel values of the LBP image
fig, ax = plt.subplots()
ax.plot(np.arange(0, 256), np.histogram(lbp, bins=np.arange(0, 257))[0])
ax.set_xlabel('LBP Prototype')
ax.set_ylabel('% of Pixels')
ax.set_title('Local Binary Pattern')

plt.show()

ax.hist(lbp, 5, density=True, facecolor='g', alpha=0.75)
plt.show()