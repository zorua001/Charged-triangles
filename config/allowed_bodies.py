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
import numpy as np

class Body:
    def __init__(self, shape_type,pos= [0,0,0],rot=[0,0,0], **kwargs):
        self.shape_type = shape_type.lower()
        self.pos = pos
        self.rot = rot
        if self.shape_type == 'cylinder':
            self.shape = Cylinder(kwargs.get('radius',1), kwargs.get('height',5), kwargs.get('radius_resolution',10), kwargs.get('height_resolution',20))
        elif self.shape_type=='sphere':
            self.shape = Sphere(kwargs.get('radius',1), kwargs.get('resolution',20))
        else:
            raise ValueError("Invalid shape type provided.")
        
        if not (isinstance(pos, list) and len(pos) == 3 and all(isinstance(item, (int, float)) for item in pos)):
            # Check if all elements are either integers or floats
            raise ValueError("In Body the pos (the position) needs to be a list of length 3 with only floats or integers")
        if not (isinstance(rot, list) and len(rot) == 3 and all(isinstance(item, (int, float)) for item in rot)):
            # Check if all elements are either integers or floats
            raise ValueError("In Body the pos (the position) needs to be a list of length 3 with only floats or integers")
        
        #Initializes the mesh
        #The pos parameter translates the object center xyz from the origin
        meshTemp= self.shape.get_mesh().translate(self.pos)
        #The rot parameter rotates the object around its center in xyz directions (radians)
        self._mesh = meshTemp.rotate(o3d.core.Tensor(create_rotation_matrix(self.rot).astype(np.float64)), o3d.core.Tensor(np.array(self.pos).astype(np.float64)))
    
    @property
    def mesh(self):
        """Getter method for the mesh."""
        return self._mesh
    
    

class Cylinder:
    def __init__(self, radius, height, radius_resolution, height_resolution):
        self.radius = radius
        self.height = height
        self.radius_resolution = radius_resolution
        self.height_resolution = height_resolution

    def get_mesh(self):
        return o3d.t.geometry.TriangleMesh.create_cylinder(self.radius,self.height, self.radius_resolution, self.height_resolution)


class Sphere:
    def __init__(self, radius, resolution):
        self.radius = radius
        self.resolution = resolution
        
    def get_mesh(self):
        return o3d.t.geometry.TriangleMesh.create_sphere

#Add more objects here!


"""
Creates a rotation matrix from an array of 3 angles in radians
"""
def create_rotation_matrix(rot):
    # Convert angles from degrees to radians
    roll = rot[0]
    pitch = rot[1]
    yaw = rot[2]
    
    # Rotation matrices around x, y, z axes
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    # Combined rotation matrix
    R = R_z @ R_y @ R_x
    return R