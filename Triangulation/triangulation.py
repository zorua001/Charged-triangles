# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:10:02 2025

@author: Hampus Berndt
"""

import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

# Define points
points = np.array([[0, 0], [1, 0], [0.5, 1], [2,3], [1,5], [0,3], [2,1],[1.5,1.5] ])

# Perform Delaunay triangulation
tri = Delaunay(points)

# Plot
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')
plt.show()
