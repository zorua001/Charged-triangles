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
from config.settings_loader import load_visualization_settings
from config.allowed_bodies import Body


def run_simulation(simulation_params, visualization_params):
    #Setup
    #Already done through loading the save
    print(f'Simulation parameters: {simulation_params}')
    
    charge_distribution_method = simulation_params['charge_distribution_method']
    bodies = simulation_params['bodies']
    # Get the areas of the triangles
    areas = [] 
    charges = []
    for body in bodies:
        s_charges = body.charges
        s_areas=body.areas_of_triangles()  
        areas.extend(s_areas)
        charges.extend(s_charges)
    
    
    #Calculate lowest and highest charge density
    if(charge_distribution_method in ['point_charge', 'homogenous']):
        if len(charges) == len(areas):
            if charge_distribution_method == 'point_charge':
                print(f'Total charge: {sum(charges)}')
                charge_density = [charge / area for charge, area in zip(charges, areas)]
            else:
                charge = [charge * area for charge, area in zip(charges, areas)]
                print(f'Total charge: {sum(charge)}')
                charge_density = charges 
        else:
            raise ValueError(f'Both lists must be of the same length. They are now {len(charges)} and {len(areas)}')   
    
    min_density = min(charge_density)
    max_density = max(charge_density)
    
    
    print(f'Minumum charge density:{min_density}')
    print(f'Maximun charge density: {max_density}')
    
    
    #Visualize everything
    #We create the colors in the bodies.
        #We then visualize all the bodies
    for body in simulation_params['bodies']:
        body.calculate_colors(simulation_params['charge_distribution_method'], visualization_params['color_method'], min_density,max_density)
        
    o3d.visualization.draw([body.mesh for body in  simulation_params['bodies']])
 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the results of a previous simulation.")
    parser.add_argument("--save", type=str, default="hvp_smoothness_p_cylinder_400_1", help="Name of the save file to use. The save files can be found under the saves directory")
    parser.add_argument("--visualization", type=str, default="settings_default", help="Name of the visualization settings file to use.")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_save(args.save)
    visualization_params = load_visualization_settings(args.visualization)
    run_simulation(simulation_params, visualization_params)

