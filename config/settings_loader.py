# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 15:53:41 2025

This is where we load and validate our settings for the simulation.

A simulation file is loaded and then validated by making sure all relevant 
parameters are present and within allowed ranges.

To change the setup, create a new settings file and run that one instead

@author: Hampus Berndt
"""


import importlib
from config.allowed_bodies import Body

#Loads the settingsfile requested
def load_settings(settings_file):
    try:
        print(1)
        module = importlib.import_module(f'settings.{settings_file}')
        print(2)
        settings = module.SIMULATION_PARAMS
        print(3)
        validate_settings(settings)  # Validate settings before returning
        return settings
    except ImportError:
        raise ValueError(f"Settings file '{settings_file}.py' not found.")


#Validates the settings, making sure that they are allowed
#Important to update the validator when adding a new setting or parameter
def validate_settings(settings):
    required_keys = ['charge_distribution_method','potential', 'bodies']
    
    for key in required_keys:
        if key not in settings:
            raise ValueError(f"Missing required setting: '{key}'")

    if not isinstance(settings['charge_distribution_method'], str) and settings['charge_distribution_method'] in ['point_charge', 'korean', 'homogenous']:
        raise ValueError("charge_distribution_method must be one of point_charge, korean, homogenous")
    
    if not (isinstance(settings['potential'], float) and settings['potential']!=0):
        raise ValueError("potential must be a non-zero float")
        
    if not isinstance(settings['bodies'], list):
        raise ValueError("Expected 'bodies' to be a list.")
        
    if not all(isinstance(item, Body) for item in settings['bodies']):
        raise ValueError("All bodies must be of the Body class")


    