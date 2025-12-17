# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 11:06:18 2025

@author: Hampus Berndt
"""

from config.allowed_bodies import Body

SIMULATION_PARAMS = {
    #Which charge distribution is used. Options are point_charge, korean, homogenous
    'charge_distribution_method': 'point_charge',
    'field_point_method': 'triple',
    'offset':float(0.5),
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': ([
                Body('cylinder',float(10), pos=[0,0,0],rot=[0,0,0], radius=1, height=3,length_resolution=20, height_resolution=20),
                Body('sphere', float(10),pos=[1.2,1.2,0], rot=[0,0,0],radius=0.5, resolution=10) 
                ])
}