import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Load the input image
img = plt.imread('redcross.png')
plt.show(img)
# Get the dimensions of the image
h, w, _ = img.shape

# Calculate center of image
center_x = w // 2
center_y = h // 2

# Initialize the radar values array with 3600 samples per angle
radar_values = np.zeros((h // 2, 3600))

# Iterate over angles and radio
for angle in np.arange(0, 360, 0.01):
    for r in range(h // 2):
        x = int(np.round(center_x + r * np.sin(np.deg2rad(angle))))
        y = int(np.round(center_y + r * np.cos(np.deg2rad(angle))))
        if x < 0 or x >= w or y < 0 or y >= h:
            radar_values[r, int(angle * 1)] = 0
        else:
            radar_values[r, int(angle * 1)] = img[y, x, 0]
