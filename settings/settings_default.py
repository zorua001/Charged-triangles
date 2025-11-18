# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 15:53:25 2025

This is an example of a settings file. It is recommended when creating new
settings to copy this file and then make changes. See settings_loader for exact
definitions on which settings are allowed.

@author: Hampus Berndt
"""
from config.allowed_bodies import Body

SIMULATION_PARAMS = {
    #The potential in the entire body
    'potential': float(5) ,
    #Which charge distribution is used. Options are point_charge, korean, homogenous
    'charge_distribution_method': 'point_charge',
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': [Body('cylinder', pos=[0,0,0],rot=[0,0,0], radius=1, height=5,length_resolution=5, height_resolution=5),]
}