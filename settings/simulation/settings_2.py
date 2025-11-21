# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 13:55:31 2025

@author: Hampus Berndt
"""

from config.allowed_bodies import Body

SIMULATION_PARAMS = {
    #Which charge distribution is used. Options are point_charge, homogenous
    'charge_distribution_method': 'point_charge',
    #Which method for finding field points is used. Options are centroid, triple
    'field_point_method': 'centroid',
    #If you have field_point_method 'triple' you need an offset variable which is a float between 0 and 1
    'offset':float(0.5),
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': [Body('sphere', float(5), pos=[0,0,0],rot=[0,0,0], radius=1, resolution=20),]
}