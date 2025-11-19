# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 11:06:18 2025

@author: Hampus Berndt
"""

from config.allowed_bodies import Body

SIMULATION_PARAMS = {
    #The potential in the entire body
    'potential': float(7) ,
    #Which charge distribution is used. Options are point_charge, korean, homogenous
    'charge_distribution_method': 'point_charge',
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': [Body('cylinder', pos=[5,0,0],rot=[1.5,0,0], radius=1, height=5,length_resolution=5, height_resolution=5),Body('cylinder', pos=[0,0,0],rot=[0,0,0], radius=1, height=5,length_resolution=5, height_resolution=5) ]
}