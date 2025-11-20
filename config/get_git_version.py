# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 12:07:45 2025
Gets the current git version of the code.

@author: Hampus Berndt
"""
import git

def get_git_version():
    try:
        # Assuming the current directory is part of a Git repository
        repo = git.Repo(search_parent_directories=True)
        return repo.head.object.hexsha  # Get the commit hash
    except Exception as e:
        print(f"Error retrieving Git version: {e}")
        return "unknown"