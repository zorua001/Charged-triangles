# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 12:07:39 2025

@author: Hampus Berndt
"""

def calculate_colors(self, charge_method, color_method):
   """Calculates the colours on all the triangles"""
   """Currently only point charge method implemented"""
   areas = self.areas_of_triangles()
   if(charge_method in ['point_charge', 'homogenous']):
       if len(self._charges) == len(areas):
           if charge_method == 'point_charge':
charge_density = [charge / area for charge, area in zip(self._charges, areas)]
                else:
                   charge_density = self._charges 
            else:
                raise ValueError(f'Both lists must be of the same length. They are now {len(self._charges)} and {len(areas)}')            
            if(color_method=='linear'):
                self._mesh.triangle.colors = o3d.core.Tensor(get_color(charge_density),o3d.core.float32) 
            elif(color_method=='log'):
                values_array = np.array(charge_density)
                charge_density_log = np.where(values_array >= 0, np.log(values_array), -np.log(np.abs(values_array)))
                self._mesh.triangle.colors = o3d.core.Tensor(get_color(charge_density_log),o3d.core.float32) 
            else:
                raise ValueError(f'{color_method} is not a valid color_method in calculate_colours in Body. Try linear' )
            return
        else:
            ValueError(f'{charge_method} is not a valid charge_method in calculate_colours in Body. Try point_charge')
   