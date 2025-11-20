# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 12:31:03 2025
Loads a saved simulation result

@author: Hampus Berndt
"""

import pickle
import os
import config.get_git_version as get_git_version

def load_save(save_name):
    subdirectory = 'saves'
    
    filename = os.path.join(subdirectory, f"{save_name}.pkl")
    
    
    # Check if the file exists
    if not os.path.isfile(filename):
       print(f"Error: The file {filename} does not exist in the saves directory.")
       exit(1)
    
    with open(filename, 'rb') as file:
        loaded_save = pickle.load(file)
    
    current_code_version = get_git_version
    
    if(current_code_version==loaded_save['code_version']):
        print('You are using the same code version as the save file!')
    else:
        print(f'You are using a different code version than the save file. Consider restoring the code to previous version. Version in save: {loaded_save['code_version']}. Version in code: {current_code_version}')

    
    return loaded_save['setting_params']
    