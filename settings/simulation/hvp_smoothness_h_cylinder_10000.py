# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 10:55:40 2025

@author: Hampus Berndt
"""

from config.allowed_bodies import Body
from config.point_potential import Point_potential

SIMULATION_PARAMS = {
    #Which charge distribution is used. Options are point_charge, homogenous
    'charge_distribution_method': 'homogenous',
    #Which method for finding field points is used. Options are centroid, triple
    'field_point_method': 'triple',
    #If you have field_point_method 'triple' you need an offset variable which is a float between 0 and 1
    'offset':float(4),
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': [Body('cylinder', float(1), pos=[0,0,0],rot=[0,0,0], radius=10, height=50,radius_resolution=50, height_resolution=100),],
    #'point_potential': [Point_potential([0,-0.5,0],float(5),radius=0.5)]
}