# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 13:10:10 2025

@author: MSI Prestige
"""

import numpy as np
import time
import concurrent.futures as future
import functools

def beräkning (charge_coordinate,point):
    korta= np.linalg.norm(np.asarray(point)-np.asarray(charge_coordinate))
    if korta != 0:
        return 1/korta
    return korta

def charge(charge_coordinates,points,potentia):
    t = time.time()
    result = np.zeros((len(points),len(charge_coordinates)))
    for j in range(len(charge_coordinates)):
        for i in range(len(points)):
            result[i,j] = 1/np.linalg.norm(points[i]-charge_coordinates[j])
            
    result[np.isnan(result)] = 0
    result[np.isinf(result)] = 0
    potentia = np.ones(len(points))*potentia        
    s = time.time()
    print(s-t)
    k = np.linalg.lstsq(result.astype('float') , potentia.astype('float'),rcond=-1)
    print(k[1])
    return k[0]

charge_coordinates = np.asarray([[1,5,7],[3,6,0],[2,3,2],[4,5,4]])
points = np.asarray([[4,2,5],[8,4,2],[7,1,2],[3,3,3]])
print(charge(charge_coordinates,points,6))
