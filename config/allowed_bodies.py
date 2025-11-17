# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 16:10:28 2025

In this file all allowed geometries of the bodies in the setup are defined.

Each body is defined as a Body which has several subcategories such as 
cylinders, sphere, cubes... Each body then creates a open3d triangulation mesh
which is used later in the program.

@author: Hampus Berndt
"""
import open3d as o3d

class Body:
    def __init__(self, shape_type,pos= [0,0,0], **kwargs):
        self.shape_type = shape_type.lower()
        self.pos = pos
        if self.shape_type == 'cylinder':
            self.shape = Cylinder(kwargs.get('radius',1), kwargs.get('height',5), kwargs.get('mesh_height',10), kwargs.get('mesh_length',20))
        else:
            raise ValueError("Invalid shape type provided.")
            
    def get_mesh(self):
        return self.shape.get_mesh()



class Cylinder:
    def __init__(self, radius, height, mesh_height, mesh_length):
        self.radius = radius
        self.height = height
        self.mesh_height = mesh_height
        self.mesh_length = mesh_length

    def get_mesh(self):
        return o3d.geometry.TriangleMesh.create_cylinder(self.radius,self.height, self.mesh_height,self.mesh_length)
#Add more objects!