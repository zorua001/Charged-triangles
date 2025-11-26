# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 16:10:28 2025

In this file all allowed geometries of the bodies in the setup are defined.

Each body is defined as a Body which has several subcategories such as 
cylinders, sphere, cubes... Each body then creates a open3d triangulation mesh
which is used later in the program.

Some other useful methods are also here that can be used in other files. 
Currently:
    -get_centroids
    -get_triangle_vertices

@author: Hampus Berndt
"""
import open3d as o3d
import numpy as np
import copy

class Body:
    def __init__(self, shape_type,potential,pos= [0,0,0],rot=[0,0,0], **kwargs):
        self.shape_type = shape_type.lower()
        self.pos = pos
        self.rot = rot
        if self.shape_type == 'cylinder':
            self.shape = Cylinder(kwargs.get('radius',1), kwargs.get('height',5), kwargs.get('radius_resolution',10), kwargs.get('height_resolution',20))
        elif self.shape_type=='sphere':
            self.shape = Sphere(kwargs.get('radius',1), kwargs.get('resolution',20))
        else:
            raise ValueError("Invalid shape type provided.")
        
        if not isinstance(potential, float):
            #Check that potential is a float
            raise ValueError("potential must be a float")
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
        self._potential = potential #Currently the potential is constant in the object
        self._charges = None #We originally have no charges in the body
        
    def __str__(self):
        """Return a string representation of the body."""
        return f"{self.shape_type} with position {self.pos}, rotation {self.rot} and other parameters"

    @property
    def mesh(self):
        """Getter method for the mesh."""
        return self._mesh
    
    @property
    def potential(self):
        """Getter method for the potential."""
        return self._potential
    
    @property
    def charges(self):
        """Get the charges."""
        return self._charges

    @charges.setter
    def charges(self, charges):
        """Set the charges."""
        #Add tests to see that charges are correct
        self._charges = charges
        
                
    def get_centroids(self):
        """Gives a list of all the centroids of the triangles"""
        triangles = self._mesh.triangle["indices"].numpy()
        vertices = self._mesh.vertex["positions"].numpy()
        centroid = np.empty([len(triangles),3])
        for i in range (len(triangles)):
            h = np.asarray([vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]])
            t = [(h[0][j]+h[1][j]+h[2][j])/3 for j in range (3)]
            centroid[i] = t    
        return centroid
    
    def get_triple_points(self, w):
        """Gives a list of three points per triangle offset from center by offset w"""
        triangles = self.get_triangles()
        vertices = self.get_vertices()
        centroids = self.get_centroids()
        triple_points = np.empty([3*len(centroids),3])
        for i in range (len(triangles)):
            h = np.asarray([vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]])
            triple_points[3*i] = [(w*h[0][j]+h[1][j]+h[2][j])/(2+w) for j in range (3)]
            triple_points[3*i+1] = [(h[0][j]+w*h[1][j]+h[2][j])/(2+w) for j in range (3)]
            triple_points[3*i+2] = [(h[0][j]+h[1][j]+w*h[2][j])/(2+w) for j in range (3)]   
        return triple_points

    def get_triangles(self):
        return self._mesh.triangle["indices"].numpy()

    def get_vertices(self):
        return self._mesh.vertex["positions"].numpy()

    def areas_of_triangles(self):
        """Calculates the areas of the triangles in the mesh"""
        triangles = self.get_triangles()
        vertices = self.get_vertices()
        surface = np.zeros(len(triangles))
        for i in range (len(triangles)):
            surface[i] = np.linalg.norm(np.cross(vertices[int(triangles[i][1])]-vertices[int(triangles[i][0])],vertices[int(triangles[i][2])]-vertices[int(triangles[i][0])]))
        return surface
    
    def get_triangle_vertices(self):
        triangles = self.get_triangles()
        vertices = self.get_vertices()
        temp = np.array([[vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]] for i in range (len(triangles))])
        return temp
    
    def calculate_colors(self, charge_method, color_method):
        """Calculates the colours on all the triangles"""
        """Currently only point charge method implemented"""
        areas = self.areas_of_triangles()
        if(charge_method in ['point_charge', 'homogenous']):
            if len(self._charges) == len(areas):
                charge_density = [charge / area for charge, area in zip(self._charges, areas)]
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
        return o3d.t.geometry.TriangleMesh.create_sphere(self.radius,self.resolution)

#Add more objects here!

"""
Returns a list of colors equally long as the list sent in.
Takes a list of values which represents relative colour.
"""
def get_color(relative_values):
    #We copy the list so that nothing happens to the original
    temp = copy.deepcopy(relative_values)
    #We get values between 0 and 1
    temp = temp/max(temp)
    #We create a color spectrum where lowest value will be green and highest red
    color = np.array([[0.5+0.5*i,0.5-0.5*i,0] for i in temp])
    return color
    


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

