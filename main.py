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
import open3d as o3d
import argparse
from config.settings_loader import load_settings
import numpy as np
from charge.calculate_charge import calculate_charge
from config.save_data import save_data



def run_simulation(simulation_params, settings_name):
    #1. Specify the bodies
        #Done in the setup file with the parameter 'bodies' where you can add
        #whichever setup you want as long as it is composed of the supported 
        #geometric shapes. Currently cylinders and spheres
        
        #To test this part on its own run the test_bodies.py file 
    bodies = simulation_params['bodies']
    
    #2. Divide the body in triangles
        #Done in the setup of the bodies
        #Currently using open3d.t.TriangleMesh. Resolution as decided through
        #the setup file
    print(f'Simulation parameters: {simulation_params}')
    
    
    #3. We determine the charge information
    
    charge_distribution_method = simulation_params['charge_distribution_method']
    
    centroids = [] 
    for body in bodies:
        s_centroids = body.get_centroids()  # Get the centroids, which is a 2D array
        centroids.append(s_centroids) 

    # Now concatenate all the collected centroids into one array
    centroids = np.vstack(centroids) if centroids else np.array([])  # Combine all into one array if not empty
    
    if charge_distribution_method == 'point_charge':
        charge_information = centroids
    else:
        ValueError('We need an allowed charge_calculation_method')

    #4. Specify the potentials in some points.
        #Currently each body has a potential from settings
        #Currently using the centroids as field points
        #todo: add that you can overdetermine the system
        #todo: change what fieldpoints we have
    field_point_method = simulation_params['field_point_method']
    if field_point_method == 'centroid':
        field_points = centroids
        field_point_potentials = np.empty(0)
        for body in bodies:
            field_point_potentials=np.concatenate((field_point_potentials,np.full(len(body._mesh.triangle["indices"].numpy()), body.potential)))
    else:
        ValueError('We need an allowed field_point_method')
    
    
    
    #5 We calculate the charges 
        #currently done using point charges
        #The charges are then put out to the bodies in the order and length 
        #that centroid were put in
        #This method relies on bodies being ordered (such as a list)
    #charges = pc.charge(centroids, centroids, potential)
    if(simulation_params['charge_distribution_method']=='point_charge'):    
        charges = calculate_charge('point_charge', charge_information,field_points,field_point_potentials)
    
    
    
    i = 0
    for body in bodies:
        body.charges = charges[i:i+len(body._mesh.triangle["indices"].numpy())]
        i+=len(body._mesh.triangle["indices"].numpy())
    del i
    
    #6.Visualize
        #We create the colors in the bodies.
        #We then visualize all the bodies
    for body in bodies:
        body.calculate_colors('point_charge')
         
    o3d.visualization.draw([body.mesh for body in bodies])
    
    
    #7. Save the result
        #We save the result so that it can be loaded again
    save_data(settings_name,simulation_params)
    
        
 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the simulation with adjustable parameters.")
    parser.add_argument("--settings", type=str, default="settings_default", help="Name of the settings file to use.")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_settings(args.settings)
    run_simulation(simulation_params, args.settings)

