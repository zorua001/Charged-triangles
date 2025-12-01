# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 13:41:05 2025

@author: MSI Prestige
"""

class Point_potential:
    def __init__(self, coordinate, potential, radius):
        self._coordinate=coordinate
        self._potential=potential
        self._radius=radius
        
        
        
    @property
    def coordinate(self):
        """Getter method for the mesh."""
        return self._coordinate
    
    @property
    def potential(self):
        """Getter method for the potential."""
        return self._potential
    
    @property
    def radius(self):
        """Get the charges."""
        return self._radius
