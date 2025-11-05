# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:35:25 2025

@author: MSI Prestige
"""

import numpy as np

def charge(points,potentia):
    distance = np.array
    for i in range(len(points)):
        for j in range(len(points)):
            korta =sum([(points[i][k]-points[j][k])**2 for k in range (3)])**0.5
            if korta != 0:
                korta = 1/korta
            distance = np.append(distance,korta) 
    distance = np.delete(distance, 0)
    distance = distance.reshape(len(points), len(points))
    potentia = np.ones(len(points))*potentia
    return np.dot(np.transpose(distance),potentia)

points = [[1,5,7],[3,6,0],[2,3,2],[4,5,4]]
print(charge(points,-5))
