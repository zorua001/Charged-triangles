# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:46:38 2025

@author: MSI Prestige
"""

import open3d as o3d
import numpy as np
import charge.homogeneous as hct

##Kanske ändra til 
mesh = o3d.geometry.TriangleMesh.create_cylinder(1,8,20,8)
mesh.compute_vertex_normals()
mesh.compute_triangle_normals()
normals = np.asarray(mesh.vertex_normals)
print(normals)
vertice = np.asarray(mesh.vertices)
triangle = np.asarray(mesh.triangles)
färg = np.array
centroid = np.array
for i in range (len(triangle)):
    h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
    t = sum(sum(h[0],h[1]),h[2])/3
    centroid = np.append(centroid,t)
centroid = np.delete(centroid, 0)
for j in range (len(vertice)):
    k = 0
    for i in range (len(triangle)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        k = hct.homogeneous(h,vertice[j]+12*normals[j])
    färg = np.append(färg,k)
färg = np.delete(färg,0)
färg = färg/max(färg)
färg_2 = np.asarray([[i,1-i,0] for i in färg])
färg_2 = färg_2.reshape(len(vertice), 3)
print (färg_2)
#mesh.paint_uniform_color([1,0,0])
mesh.vertex_colors = o3d.utility.Vector3dVector(färg_2)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
print(k)