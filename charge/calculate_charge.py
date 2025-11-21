# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:58:20 2025

@author: Hampus Berndt
"""

import numpy as np
from charge.homogeneous import homogeneous_memo


def calculate_charge(method,charge_information,field_points,field_point_potentials):
    coefficients = np.zeros((len(field_points),len(charge_information)))
    if method=='point_charge': 
        ##Uses Coloumbs law from point charges to calculate
        ##Wants charge_information to be the coordinate of the point charge
        for j in range(len(charge_information)):
            for i in range(len(field_points)):
                coefficients[i,j] = 1/np.linalg.norm(field_points[i]-charge_information[j])
    
    elif method=='homogenous':
        ##Uses HCT method
        ##Wants charge_information to be the vertex coordinates of the triangle
        ##corresponding to that point charge
        for j in range(len(charge_information)):
            for i in range(len(field_points)):
                coefficients[i,j] = homogeneous_memo(charge_information[j], field_points[i],j)
    else:
        ValueError("Method in calculate_charge must be an allowed method")        
    
    coefficients[np.isnan(coefficients)] = 0
    coefficients[np.isinf(coefficients)] = 0
    return np.linalg.lstsq(coefficients.astype('float') , field_point_potentials,rcond=-1)[0]
