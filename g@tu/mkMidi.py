import os
import mido
import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt('testLux.csv', delimiter=',', skiprows=1)

# Extract time and lux values
time = data[:, 0]
lux = data[:, 1]
