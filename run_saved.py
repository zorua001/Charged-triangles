# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 13:38:56 2025

Loads a saved simulation result and visualizes it again.

You call the function by going to the project directory and then running the 
script. You have to include a save name that exists in the saves directory.
Do not include the directory or .pkl extension.

Example:
    #change direction of / bc unicode
    cd C:/Users/MyName/TrianglesAndSpacecraft
    python run_saved.py --save simulation_setup_1_3

@author: Hampus Berndt
"""


import argparse
import open3d as o3d
from config.load_save import load_save


def run_simulation(simulation_params):
    #Setup
    #Already done through loading the save
    print(f'Simulation parameters: {simulation_params}')
    
    #Visualize everything
    o3d.visualization.draw([body.mesh for body in simulation_params['bodies']])
    
 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the results of a previous simulation.")
    parser.add_argument("--save", type=str, required=True, help="Name of the save file to use. The save files can be found under the saves directory")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_save(args.save)
    run_simulation(simulation_params)

