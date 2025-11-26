# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 12:31:16 2025
In here we save the result of the simulation

Setting_params are saved, which notably includes bodies which hold all charges,
colors and other relevant data

We also save the current version of the code so that we can redo experiments

@author: Hampus Berndt
"""

import pickle
import os
import config.get_git_version as get_git_version
import dill

#Because setting_params holds bodies we only need to save setting params and 
#can then run 
def save_data(simulation_name, setting_params):

    # Example of simulation result
    #Maybe include time here later? Or other measure of how long it took to compute?
    simulation_result = {'setting_params': setting_params, 'code_version': get_git_version,}

    # Get a unique filename
    unique_filename = get_unique_filename('saves',simulation_name)

    # Save the result
    with open(unique_filename, 'wb') as file:
        #pickle.dump(simulation_result, file)
        dill.dump(simulation_result, file)

    print(f"Saved simulation results to {unique_filename}")
    
# Function to generate a unique filename based on a base name
def get_unique_filename(subdirectory,base_name):
    
    # Ensure the subdirectory exists
    os.makedirs(subdirectory, exist_ok=True)
    
    index = 1
    filename = os.path.join(subdirectory, f"{base_name}_{index}.pkl")
    
    # Increment index until a unique filename is found
    while os.path.exists(filename):
        index += 1
        filename = os.path.join(subdirectory, f"{base_name}_{index}.pkl")
    
    return filename