# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 16:21:39 2025

@author: MSI Prestige
"""

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.tri import Triangulation
import Homogeneous as hct


#behöver radie och mittpunkt på sfär
def sphere(r,c):
    theta= np.linspace(0, 2*np.pi,20)
    phi =np.linspace(0, np.pi,20)
    theta,phi = np.meshgrid(theta,phi)
    
    x = np.ravel(r*np.cos(theta)*np.sin(phi))
    y = np.ravel(r*np.sin(theta)*np.sin(phi))
    z = np.ravel(r*np.cos(phi))
    
    tri = Triangulation(np.ravel(theta), np.ravel(phi))
    
    return x,y,z,tri
    

def centroids_sphere(tri,r):
    centroid = np.array
    triangles = tri.triangles
    x = np.array(r*np.sin(tri.y)*np.cos(tri.x))
    y = np.array(r*np.sin(tri.y)*np.sin(tri.x))
    z = np.array(r*np.cos(tri.y))
    for i in range (len(triangles)):
        k = [x[triangles[i][0]]+x[triangles[i][1]+x[triangles[i][2]]]]
    
    
    
    return
    
    
def cyinder():  
    z = np.linspace(0, 2,20)
    r = np.linspace(0, 2,20)
    theta = np.linspace(0, 2*np.pi,20)
    
    
    theta,z = np.meshgrid(theta,z)
    
    
    x = np.ravel(2*np.cos(theta))
    y = np.ravel(2*np.sin(theta))
    z = np.ravel(z)
    
    tri = Triangulation(np.ravel(z), np.ravel(theta))
    # Source - https://stackoverflow.com/a
    # Posted by jlandercy, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-11-13, License - CC BY-SA 4.0
    print (tri.triangles)
    return


# Render:
x,y,z,tri = sphere(2, [1,1,1])
ax = plt.axes(projection='3d')
ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap='viridis', antialiased=True) 
