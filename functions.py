# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 10:47:49 2025

@author: Hampus Berndt
"""
import numpy as np


"""Takes a """
def get_centroids(triangles, vertices):
    centroid = np.empty([len(triangles),3])
    for i in range (len(triangles)):
        h = np.asarray([vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]])
        t = sum(sum(h[0],h[1]),h[2])/3
        centroid[i] = t    
    return centroid