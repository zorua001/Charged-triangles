# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 13:10:10 2025

@author: MSI Prestige
"""

import numpy as np
import concurrent.futures as future
import functools

def beräkning (charge_coordinate,point):
    korta= np.linalg.norm(np.asarray(point)-np.asarray(charge_coordinate))
    if korta != 0:
        return 1/korta
    return korta

def charge(charge_coordinates,points,potentia):
    result = np.zeros((len(charge_coordinates),len(points)))
    for j in range(len(charge_coordinates)):
        for i in range(len(points)):
            result[j,i] = 1/np.linalg.norm(points[i]-charge_coordinates[j])
        
    print (result)
    result[np.isnan(result)] = 0
    result[np.isinf(result)] = 0
    potentia = np.ones(len(charge_coordinates))*potentia        
    return np.linalg.lstsq(result.astype('float') , potentia.astype('float'),rcond=-1)[0]

charge_coordinates = np.asarray([[1,5,7],[3,6,0],[2,3,2],[4,5,4]])
points = np.asarray([[1,4,7],[8,4,2],[7,1,2],[3,3,3]])
print(charge(charge_coordinates,points,6))
