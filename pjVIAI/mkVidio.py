import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# Load image
img = plt.imread('redcross.png')

imgArray = np.asarray(img)
print(repr(img))

imgplot = plt.imshow(img)

# Get the dimensions of the image
h, w, _ = img.shape

# Calculate center of image
center_x = w // 2
center_y = h // 2

print(center_x, center_y)

# Image with the center marked
plt.imshow(img)
plt.scatter(center_x, center_y, marker="+", color="green", s=200)
plt.show()

# Initialize the radar values array with 3600 samples per angle
radar_values = np.zeros((h // 2, 3600))

# Iterate over angles and radio
for angle in np.arange(0, 3600, 1.0):
    for r in range(h // 2):
        x = int(np.round(center_x + r * np.sin(np.deg2rad(angle))))
        y = int(np.round(center_y + r * np.cos(np.deg2rad(angle))))
        if x < 0 or x >= w or y < 0 or y >= h:
            radar_values[r, int(angle * 1)] = 0
        else:
            radar_values[r, int(angle * 1)] = img[y, x, 0]

# Calculate average values at each angle
avg_values = np.mean(radar_values, axis=0)

# Save radar sweep to text file
data = np.column_stack((np.arange(0, 3600, 1.0), avg_values))
# save the data as a CSV file
np.savetxt('radarSweep.csv', data, delimiter=',', header='C1,C2', comments='', fmt='%.3f')

# Plot polar values
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(np.deg2rad(np.arange(0, 3600, 1.0)), avg_values)

# set limits of x and y-axis
xLim = ax.set_xlim([0, img.shape[1]])
yLim = ax.set_ylim([0, img.shape[0]])
print(xLim, yLim)

# remove ticks and numbers
ax.set_xticks([])
ax.set_yticks([])

# calculate center of image
center_x = img.shape[1] / 2
center_y = img.shape[0] / 2
max_distance = np.sqrt((img.shape[0] / 2) ** 2 + (img.shape[1] / 2) ** 2)

print(max_distance)

# create line for radar sweeping
line, = ax.plot([center_x, center_x], [center_y, center_y - 50], color='blue',
                linewidth=2, solid_capstyle='round')

# define parameters for pulsation
freq = 10
amp = 5

# define function to update line position in animation
def update_line(num):
    angle = np.deg2rad(num)
    r = max_distance + amp * np.sin(2.0 * np.pi * freq * num / num_frames)
    x = center_x + r * np.cos(angle)
    y = center_y - r * np.sin(angle)
    line.set_data([center_x, x], [center_y, y])
    alpha = 1  # (1-r/100)**3 # calculate alpha value based on distance from center
    line.set_linewidth(2)  # (2 + 4*(1-r/1000)) # set line thickness based on distance from center
    line.set_alpha(alpha)  # set alpha value to create beam-like effect
    line.set_solid_capstyle('round')
    return line,


# create animation object
num_frames = 1440  # 72 seconds at 50ms per frame
frames = np.linspace(0, 360, num_frames, endpoint=False)
ani = animation.FuncAnimation(fig, update_line, frames=frames,
                              interval=50)

# create video writer
Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='VikoLuna'), bitrate=1800)

# save animation as video
ani.save('videoMov.mp4', writer=writer)

# add audio to the mp4 file
os.system('ffmpeg -i wizardio.mp3 wizardio.wav')
os.system('ffmpeg -i wizardio.mp3 -i mago.mp4 -map 0:a -map 1:v -c copy -shortest nuevoColor.mp4')
