# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 12:52:43 2025

@author: MSI Prestige
"""

from config.allowed_bodies import Body
from config.point_potential import Point_potential


## changing anything about the bodies apart from the potential forces name change
SIMULATION_PARAMS = {
    'name': 'box_cylinder_cylinder_homo_triple_4',
    #Which charge distribution is used. Options are point_charge, homogenous
    'charge_distribution_method': 'homogenous',
    #Which method for finding field points is used. Options are centroid, triple
    'field_point_method': 'triple',
    #If you have field_point_method 'triple' you need an offset variable which is a float between 0 and 1
    'offset':float(0.5),
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': ([
        Body('cylinder', float(5), pos=[.25,.25,-2.5],rot=[0,0,0], radius=0.25, height=5,length_resolution=10, height_resolution=10),
        Body('box', float(5) ,pos = [0,0,0],rot =[0,0,0], height=3 , width = 3, depth = 3, iterations = 3 ),
        Body('cylinder', float(5), pos=[2.75,.25,-2.5],rot=[0,0,0], radius=0.25, height=5,length_resolution=10, height_resolution=10)
        ]),
    'point_potential':  [Point_potential([0,.5,.5],float(5),radius=0.25)]
}