# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import open3d as o3d
import numpy as np
import charge.homogeneous as hct
import Parallell_charges as ch
import time

def homogen (center,triangle,vertice):
    färg = np.array
    for j in range (len(center)):
        k = 0
        for i in range (len(triangle)):
            h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
            k = k + hct.homogeneous(h,center[j])
        färg = np.append(färg,k)
    färg = np.delete(färg,0)
    färg = färg/max(färg)
    färg_2 = np.asarray([[i,1-i,0] for i in färg])
    färg_2 = färg_2.reshape(len(center), 3)
    return färg_2

#beräknar laddning på punktladdning
def point_ch(centroid,vertice,triangle):
    surface = area(vertice, triangle)
    k = ch.charge(centroid, centroid, -5)
    k = k/surface
    k = k/max(abs(k))
    färg = np.array([[0.5+0.5*i,0.5-0.5*i,0] for i in k])
    return färg    

#Beräknar laddning utifrån homogen fördelning
def homogeneous_ch(centroid,vertice,triangle):
    t = np.array([[vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]] for i in range (len(triangle))])
    surface = area(vertice, triangle)
    k = hct.charge(t, centroid, -5)
    k = k/surface
    k = k/max(abs(k))
    färg = np.array([[0.5+0.5*i,0.5-0.5*i,0] for i in k])
    return färg    
    
    
def centroid(mesh):
    vertice = mesh.vertex["positions"].numpy()
    triangle = mesh.triangle["indices"].numpy()
    centroid = np.empty([len(triangle),3])
    for i in range (len(triangle)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        t = [(h[0][j]+h[1][j]+h[2][j])/3 for j in range (3)]
        centroid[i] = t
    return centroid,vertice,triangle

def area(vertice,triangle):
    surface = np.zeros(len(triangle))
    for i in range (len(triangle)):
        surface[i] = np.linalg.norm(np.cross(vertice[int(triangle[i][1])]-vertice[int(triangle[i][0])],vertice[int(triangle[i][2])]-vertice[int(triangle[i][0])]))
    return surface
    
##Kanske ändra till o3d.t 
mesh = o3d.t.geometry.TriangleMesh.create_cylinder(1,3,20,10)
#print(mesh.vertex["positions"].numpy())

mesh2 = o3d.t.geometry.TriangleMesh.create_sphere(.5,10)
mesh2 = mesh2.translate(o3d.core.Tensor([1.2,1.2,0]))


center,vertice,triangle = centroid(mesh)
center_2,vertice_2,triangle_2 = centroid(mesh2)
tot = np.concatenate((center,center_2))
t = time.time()
färg = homogeneous_ch(center,vertice,triangle)

#färg_2 = homogen(center,vertice,triangle)
s = time.time()
print(s-t)
mesh.triangle.colors = o3d.core.Tensor(färg[:len(center)],o3d.core.float32)
mesh.compute_vertex_normals()


#mesh2.triangle.colors = o3d.core.Tensor(färg,o3d.core.float32)
mesh2.compute_vertex_normals()

o3d.visualization.draw([mesh])
