"""
This file is used to get image of grid_data
"""

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import numpy as np
import time
import os

for i in range(1,6):
    a = np.load(f"grid_data\grid_snn_nn_03_{i}.npy")
    plt.figure()
    plt.imshow(a, cmap='binary')
    plt.title('Diffusion-limited aggregation (Pnn=0.3, Psnn=0.15)')
    plt.show()

# Interval = range(502,4003,500)
# for i in Interval:
#     filename="images/cluster"+str(i)+".png"
#     os.remove(filename)

