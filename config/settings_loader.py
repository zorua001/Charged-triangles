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
from config.point_potential import Point_potential

#Loads the settingsfile requested
def load_simulation_settings(settings_file):
    try:
        module = importlib.import_module(f'settings.simulation.{settings_file}')
        settings = module.SIMULATION_PARAMS
        validate_settings_simulation(settings)  # Validate settings before returning
        return settings
    except ImportError:
        raise ValueError(f"Simulation setting file '{settings_file}.py' not found.")

def load_visualization_settings(settings_file):
    try:
        module = importlib.import_module(f'settings.visualization.{settings_file}')
        settings = module.VISUALIZATION_PARAMS
        validate_settings_visualization(settings)  # Validate settings before returning
        return settings
    except ImportError:
        raise ValueError(f"Visualization setting file '{settings_file}.py' not found.")

#Validates the settings for the simulation, making sure that they are allowed
#Important to update the validator when adding a new setting or parameter
def validate_settings_simulation(settings):
    required_keys = ['charge_distribution_method','field_point_method', 'bodies']
    
    
    for key in required_keys:
        if key not in settings:
            raise ValueError(f"Missing required setting: '{key}'")

    if not isinstance(settings['charge_distribution_method'], str) and settings['charge_distribution_method'] in ['point_charge', 'korean', 'homogenous']:
        raise ValueError("charge_distribution_method must be one of point_charge and homogenous")
    
    if not isinstance(settings['field_point_method'], str) and settings['field_point_method'] in ['centroid', 'triple']:
        raise ValueError("charge_distribution_method must be one of centroid or triple")
       
        # Check for the optional 'offset' parameter when 'field_point_method' is 'triple'
    if settings['field_point_method'] == 'triple':
        if 'offset' not in settings:
            raise ValueError("Missing required setting: 'offset' when 'field_point_method' is 'triple'")
        # Offset must be single float between 0 and 1
        if not isinstance(settings['offset'], (int, float)):
            raise ValueError("offset must be a single number.")
        if not (0 < settings['offset'] < 1):
            raise ValueError("offset must be between 0 and 1.")
        
    if not isinstance(settings['bodies'], list):
        raise ValueError("Expected 'bodies' to be a list.")
        
    if not all(isinstance(item, Body) for item in settings['bodies']):
        raise ValueError("All bodies must be of the Body class")
        
    if settings['point_potential']:
        if not all(isinstance(item, Point_potential) for item in settings['point_potential']):
            raise ValueError("All point potentials must be of class Point_charge")
            

#Validates the settings for the visualizations, making sure that they are allowed
#Important to update the validator when adding a new setting or parameter
def validate_settings_visualization(settings):
    required_keys = ['color_method']
    
    for key in required_keys:
        if key not in settings:
            raise ValueError(f"Missing required setting: '{key}'")

    if not isinstance(settings['color_method'], str) and settings['color_method',] in ['linear', 'log']:
        raise ValueError("color_method must be one of linear or log")