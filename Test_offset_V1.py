# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 13:22:47 2025

@author: MSI Prestige

If no .npy files are 
"""

import open3d as o3d 
import numpy as np
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

def area(triangle):
    surface = np.zeros(len(triangle))
    for i in range(len(triangle)):
        surface[i] = np.linalg.norm(np.cross(triangle[i][1]-triangle[i][0],triangle[i][2]-triangle[i][0]))/2
    return surface


a = np.linspace(0.1, 10,100)

mesh = o3d.t.geometry.TriangleMesh.create_cylinder(1,3,5,10)
b = np.zeros(len(a))
for i in range(len(a)):
    center_test,vertice_test,triangle_test,extended_test = get_triple_points(mesh,a[i])
    triangle_test = get_triangles(vertice_test, triangle_test)
    d = np.ones(len((extended_test)))*5
    lad = calculate_charge('homogenous',  triangle_test ,extended_test,d, a[i])
    surface = area(triangle_test)
    ## For 
    b[i] = sum([lad[j]*surface[j] for j in range(len(lad))])
print(b)

plt.xlabel('Offset')
plt.ylabel('Sum of charges')
plt.title('How offset affects homogenous triangles')
plt.plot(a,b,'*')



c = np.zeros(len(a))
for i in range(len(a)):
    center_test,vertice_test,triangle_test,extended_test = get_triple_points(mesh,a[i])
    triangle_test = get_triangles(vertice_test, triangle_test)
    d = np.ones(len((extended_test)))*5
    lad = calculate_charge('point_charge',  center_test ,extended_test,d, f'{a[i]}point')
    c[i] = sum(lad)
       
a = np.delete(a, 9)
c = np.delete(c,9)

plt.figure()
plt.xlabel('Offset')
plt.ylabel('Sum of charges')
plt.title('How offset affects point charges')
plt.plot(a,c,'*')