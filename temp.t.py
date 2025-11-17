# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import open3d as o3d
import numpy as np
import Homogeneous as hct
import Charges as ch

def homogen (centroid,triangle,vertice,färg):
    for j in range (len(centroid)):
        k = 0
        for i in range (len(triangle)):
            h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
            k = k + hct.homogeneous(h,centroid[j])
        färg = np.append(färg,k)
    färg = np.delete(färg,0)
    färg = färg/max(färg)
    färg_2 = np.asarray([[i,1-i,0] for i in färg])
    färg_2 = färg_2.reshape(len(centroid), 3)
    print(len(färg_2))
    print (färg_2)
    return färg_2


def point_ch(centroid):
    k = ch.charge(centroid, centroid, 4)
    k = k/max(k)
    färg = np.array([[i,1-i,0] for i in k])
    return färg    
    
##Kanske ändra till o3d.t 
mesh = o3d.t.geometry.TriangleMesh.create_cylinder(1,3,40,80)
#print(mesh.vertex["positions"].numpy())


vertice = mesh.vertex["positions"].numpy()
triangle = mesh.triangle["indices"].numpy()
färg = np.array
centroid = np.empty([len(triangle),3])

for i in range (len(triangle)):
    h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
    t = sum(sum(h[0],h[1]),h[2])/3
    centroid[i] = t

färg_2 = point_ch(centroid)
mesh.triangle.colors = o3d.core.Tensor(färg_2,o3d.core.float32)
mesh.compute_vertex_normals()

o3d.visualization.draw([mesh])
