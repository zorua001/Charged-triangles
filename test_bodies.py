# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 12:47:02 2025

This function draws and shows the bodies in your setup file without any other 
calculations so you can swiftly test that the setup is correct

example of how to run :
    cd C:/Users/Name/triangles_and_spacecraft #go to the project directory
    python test_bodies.py #Run with default settings
    python test_bodies.py --settings=my_settings #Uses the file my_settings which you have created


@author: Hampus Berndt
"""


import argparse
from config.settings_loader import load_settings
import open3d as o3d



def run_simulation(simulation_params):
    #Setup
    #Already done through setting setup
    print(f'Simulation parameters: {simulation_params}')
    
    
    #Create the bodies
    o3d.visualization.draw([body.mesh for body in simulation_params['bodies']])
    
        
 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the simulation with adjustable parameters.")
    parser.add_argument("--settings", type=str, default="settings_default", help="Name of the settings file to use.")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_settings(args.settings)
    run_simulation(simulation_params)

