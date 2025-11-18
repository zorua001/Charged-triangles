# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:35:25 2025

@author: MSI Prestige
"""

import numpy as np

def beräkning (charge_coordinate,point):
    korta =sum([(point[k]-charge_coordinate[k])**2 for k in range (3)])**0.5
    if korta != 0:
        return 1/korta
    return korta

def charge(charge_coordinates,points,potentia):
    print("hello")
    distance = np.zeros([len(charge_coordinates),len(points)])
    for i in range(len(points)):
        for j in range(len(points)):
            korta =sum([(points[i][k]-charge_coordinates[j][k])**2 for k in range (3)])**0.5
            if korta != 0:
                korta = 1/korta
            distance[i][j] = korta 
    potentia = np.ones(len(points))*potentia
    print("hej")
    return np.linalg.lstsq(distance.astype('float') , potentia.astype('float'),rcond=-1)[0]

charge_coordinates = [[1,5,7],[3,6,0],[2,3,2],[4,5,4]]
points = [[4,2,5],[8,4,2],[7,1,2],[3,3,3]]
print(charge(charge_coordinates,points,6))
