# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 10:20:00 2025

This is the main file where everything is controlled.

To run a simulation enter the console in this directory and run this script. 
If you want specific settings add them after the file.

example:
    cd C:/Users/Name/triangles_and_spacecraft #bc unicode had to use wrong direction on /
    python main.py #Uses default settings
    python main.py --settings=my_settings #Uses the file my_settings which you have created

@author: Hampus Berndt
"""

import argparse
from config.settings_loader import load_settings



def run_simulation(simulation_params):
    print(simulation_params)
    
    # Simulation logic here
 
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the simulation with adjustable parameters.")
    parser.add_argument("--settings", type=str, default="settings_default", help="Name of the settings file to use.")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_settings(args.settings)
    run_simulation(simulation_params)

