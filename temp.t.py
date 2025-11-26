# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import open3d as o3d
import numpy as np
import charge.homogeneous as hct
import parallell_2 as ch
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
def point_ch(centroid,extended,triangle,decision):
    surface = area_tri(triangle)
    if decision:
        k = ch.charge(centroid, extended, -5)
    else:
        k = ch.charge(centroid,centroid,-5)
    print(k)
    print(sum(k))
    for i in range(len(k)):
        if k[i] >= 0: 
            k[i] =  np.log(k[i]/surface[i])
        else:
            k[i] = -np.log(abs(k[i])/surface[i])
    k = k/max(abs(k))
    färg = np.array([[i,1-i,0] for i in k])
    return färg    

#Beräknar laddning utifrån homogen fördelning
def homogeneous_ch(centroid,triangles):
    surface = area_tri(triangles)
    k = hct.charge_2(triangles, centroid, 5)
    print(sum(k))
   
    for i in range(len(k)):
        if k[i] >= 0: 
            k[i] =  np.log(k[i])
        else:
            k[i] = -np.log(abs(k[i]))
    k = k/max(abs(k))
    färg = np.array([[0.5+0.5*i,0.5-0.5*i,0] for i in k])
    return färg    
    
    
def centroid(mesh):
    vertice = mesh.vertex["positions"].numpy()
    triangle = mesh.triangle["indices"].numpy()
    centroid = np.empty([len(triangle),3])
    extended = np.empty([3*len(triangle),3])
    w = 0.5
    for i in range (len(triangle)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        t = [(h[0][j]+h[1][j]+h[2][j])/3 for j in range (3)]
        centroid[i] = t
        extended[3*i] = [(w*h[0][j]+h[1][j]+h[2][j])/(2+w) for j in range (3)]
        extended[3*i+1] = [(h[0][j]+w*h[1][j]+h[2][j])/(2+w) for j in range (3)]
        extended[3*i+2] = [(h[0][j]+h[1][j]+w*h[2][j])/(2+w) for j in range (3)]
    print(len(extended))
    return centroid,vertice,triangle,extended

def area(vertice,triangle):
    surface = np.zeros(len(triangle))
    for i in range (len(triangle)):
        surface[i] = np.linalg.norm(np.cross(vertice[int(triangle[i][1])]-vertice[int(triangle[i][0])],vertice[int(triangle[i][2])]-vertice[int(triangle[i][0])]))/2
    print(len(surface))
    return surface

def area_tri(triangle):
    surface = np.zeros(len(triangle))
    for i in range(len(triangle)):
        surface[i] = np.linalg.norm(np.cross(triangle[i][1]-triangle[i][0],triangle[i][2]-triangle[i][0]))/2
    return surface





def more_points(centroid):
    points = np.array
    points = np.delete(points, 0)
    w = 0.5
    for i in range (len(centroid)):
        points = np.append(points, [w*centroid[i][0],centroid[i][1],centroid[i][2]])
        points = np.append(points, [centroid[i][0],w*centroid[i][1],centroid[i][2]])
        points = np.append(points, [centroid[i][0],centroid[i][1],w*centroid[i][2]])
    points = points.reshape((len(centroid)*3,3))
    print(len(points))
    return points

def get_triangles(vertice, triangle):
    t = np.array([[vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]] for i in range (len(triangle))])
    return t
##Kanske ändra till o3d.t 
mesh = o3d.t.geometry.TriangleMesh.create_cylinder(1,3,20,20)




#print(mesh.vertex["positions"].numpy())

mesh2 = o3d.t.geometry.TriangleMesh.create_sphere(.5,10)
mesh2 = mesh2.translate(o3d.core.Tensor([1.2,1.2,0]))


center,vertice,triangle,extended = centroid(mesh)
center_2,vertice_2,triangle_2,extended_2 = centroid(mesh2)
tot = np.concatenate((center,center_2))
triangles = get_triangles(vertice, triangle)
triangles_2 = get_triangles(vertice_2, triangle_2)
tot_a = np.concatenate((triangles,triangles_2))
tot_c = np.concatenate((extended,extended_2))


#Ändra från true eller false om man ska använda fler punkter eller inte
decision = 1


t = time.time()
#färg = point_ch(tot,tot_c,tot_a,decision)
#färg = homogeneous_ch(center_2, triangles_2)

färg_2 = homogeneous_ch(tot,tot_a)
s = time.time()
print(s-t)
mesh.triangle.colors = o3d.core.Tensor(färg_2[:len(center)],o3d.core.float32)
mesh.compute_vertex_normals()

more_points(np.array([[1,2,3]]))

mesh2.triangle.colors = o3d.core.Tensor(färg_2[len(center):],o3d.core.float32)
mesh2.compute_vertex_normals()

o3d.visualization.draw([mesh,mesh2])
