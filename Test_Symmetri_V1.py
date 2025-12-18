# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 11:33:40 2025

@author: MSI Prestige
"""

import numpy as np
import open3d as o3d
import charge.homogeneous as hct
from charge.calculate_charge import calculate_charge
import matplotlib.pyplot as plt

def get_triple_points(mesh, w):
     """Gives a list of three points per triangle offset from center by offset w"""
     triangles = mesh.triangle["indices"].numpy()
     vertices = mesh.vertex["positions"].numpy()
     centroid = np.empty([len(triangles),3])
     for i in range (len(triangles)):
         h = np.asarray([vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]])
         t = [(h[0][j]+h[1][j]+h[2][j])/3 for j in range (3)]
         centroid[i] = t    
     triple_points = np.empty([3*len(centroid),3])
     for i in range (len(triangles)):
         h = np.asarray([vertices[int(triangles[i][0])],vertices[int(triangles[i][1])],vertices[int(triangles[i][2])]])
         triple_points[3*i] = [(w*h[0][j]+h[1][j]+h[2][j])/(2+w) for j in range (3)]
         triple_points[3*i+1] = [(h[0][j]+w*h[1][j]+h[2][j])/(2+w) for j in range (3)]
         triple_points[3*i+2] = [(h[0][j]+h[1][j]+w*h[2][j])/(2+w) for j in range (3)]   
     return centroid,vertices,triangles,triple_points
 
     
def get_triangles(vertice, triangle):
    t = np.array([[vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]] for i in range (len(triangle))])
    return t

 

def calculate_potential(triangles,charges,point,metod):
    tot_pot = 0
    if metod == 'homogenous':
        for i in range(len(triangles)):
            tot_pot = tot_pot + hct.homogeneous(triangles[i],point)*charges[i]
    else:
        for i in range(len(triangles)):
            tot_pot = tot_pot + charges[i]/np.linalg.norm(triangles[i]-point)
            
    return tot_pot



def symmetri(mesh,decision,name):
    center,vertices,triangles,field_points = get_triple_points(mesh, 4)
    triangle = get_triangles(vertices, triangles)
    d = np.ones(len((field_points)))*500
    
    """
    Välj 1 för homogeneous och 0 för point charges 
    """
    
    if decision:
        lad = calculate_charge('homogenous',  triangle ,field_points,d, f'test_{name}_homo')
    else:
        lad = calculate_charge('point_charge',  center ,field_points,d, f'test_{name}_punkt')
        
    vinkel = np.linspace(0, 2*np.pi,50)
    r = 1
    jämförelse = np.zeros(len(vinkel))
    if decision:
        for i in range(len(vinkel)):
            jämförelse[i] = calculate_potential(triangle, lad, np.array([r*np.cos(vinkel[i]),r*np.sin(vinkel[i]),0]), 'homogenous')
            print(np.cos(vinkel[i]))
    else:
        for i in range(len(vinkel)):
            jämförelse[i] = calculate_potential(center, lad, np.array([r*np.cos(vinkel[i]),r*np.sin(vinkel[i]),0]), 'point_charge')
    
    plt.figure()
    plt.plot(vinkel,jämförelse)
    plt.xlabel('Angle (rad)')
    plt.ylabel('Potential')
    if decision:
        plt.title(f'Potential in a circle of radius {r} around {name} (Homogenous)')
    else:
        plt.title(f'Potential in a circle of radius {r} around {name} (Point_charge)')
    


#mesh = o3d.t.geometry.TriangleMesh.create_sphere(2,10)
#symmetri(mesh,1,'sfär')

mesh_2 = o3d.t.geometry.TriangleMesh.create_cylinder(1,5,50,50)
symmetri(mesh_2,0,'cylinder_50')



