# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 10:59:22 2025

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
    print("hello")
    distance = np.zeros([len(charge_coordinates),len(points)])
    for i in range (len(charge_coordinates)):
        k = functools.partial(beräkning,points[i])
        with future.ThreadPoolExecutor() as executor:
            distance[i] = list(executor.map(k, charge_coordinates))
    potentia = np.ones(len(points))*potentia
    print("hej")
    t = np.linalg.lstsq(distance.astype('float') , potentia.astype('float'),rcond=-1)[0]
    return t

charge_coordinates = [[1,5,7],[3,6,0],[2,3,2],[4,5,4]]
points = [[4,2,5],[8,4,2],[7,1,2],[3,3,3]]
print(charge(charge_coordinates,points,6))
