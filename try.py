# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 14:14:53 2025

@author: MSI Prestige
"""

import open3d as o3d
import numpy as np
import charge.homogeneous as hct
import Parallell_charges as ch
import concurrent.futures as future
import functools
import time

def homogen (center,triangle,vertice):
    färg = np.zeros(len(center))
    for i in range (len(center)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        t = functools.partial(hct.homogeneous, h)
        with future.ThreadPoolExecutor() as ex:
            färg[i] = sum(list(ex.map(t, center)))
    färg = färg/max(färg)
    färg_2 = np.asarray([[i,1-i,0] for i in färg])
    färg_2 = färg_2.reshape(len(center), 3)
    return färg_2


def point_ch(centroid):
    k = ch.charge(centroid, centroid, 4)
    k = k/max(k)
    färg = np.array([[i,1-i,0] for i in k])
    return färg    
    
def centroid(mesh):
    vertice = mesh.vertex["positions"].numpy()
    triangle = mesh.triangle["indices"].numpy()
    centroid = np.empty([len(triangle),3])
    for i in range (len(triangle)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        t = sum(sum(h[0],h[1]),h[2])/3
        centroid[i] = t
    return centroid,triangle,vertice

def color (centroid):
    
    färg_2 = point_ch(centroid)
    return färg_2
    
##Kanske ändra till o3d.t 
mesh = o3d.t.geometry.TriangleMesh.create_cylinder(1,3,10,20)
#print(mesh.vertex["positions"].numpy())

mesh2 = o3d.t.geometry.TriangleMesh.create_sphere(.5,10)
mesh2 = mesh2.translate(o3d.core.Tensor([1.2,1.2,0]))


center,vertice,triangle = centroid(mesh)
center_2,vertice_2,triangle_2 = centroid(mesh2)
tot = np.concatenate((center,center_2))
#färg = color(tot)
t = time.time()
färg_2 = homogen(center_2,vertice_2,triangle_2)
s = time.time()
print(s-t)
mesh2.triangle.colors = o3d.core.Tensor(färg_2,o3d.core.float32)
mesh.compute_vertex_normals()


#mesh2.triangle.colors = o3d.core.Tensor(färg[len(center):],o3d.core.float32)
mesh2.compute_vertex_normals()

o3d.visualization.draw([mesh2])