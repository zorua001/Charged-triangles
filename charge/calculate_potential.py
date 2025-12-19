# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 12:31:21 2025

Calculates the potential 

@author: Hampus Berndt
"""
import numpy as np
import charge.homogeneous as hct

def calculate_potential(triangles,charges,point,metod):
    tot_pot = 0
    if metod == 'homogenous':
        for i in range(len(triangles)):
            tot_pot = tot_pot + hct.homogeneous(triangles[i],point)*charges[i]
    else:
        for i in range(len(triangles)):
            tot_pot = tot_pot + charges[i]/np.linalg.norm(triangles[i]-point)
            
    return tot_pot

