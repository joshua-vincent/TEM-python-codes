# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 10:03:19 2020

View .dat file from DrProbe simulations

@author: Josh
"""

import numpy as np
import matplotlib.pyplot as plt

image_file = r'C:\Users\Josh\Downloads\image.dat'

nx = ny = 512

img = np.fromfile(image_file, dtype=np.single).reshape((nx,ny))

plt.imshow(img, cmap='gray', vmin=0.8, vmax=1.2)