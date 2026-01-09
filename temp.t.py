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
        k = ch.charge(centroid, extended, 5)
    else:
        k = ch.charge(centroid,centroid,-5)
    chai = k
    print(sum(chai))
    for i in range(len(k)):
        if k[i] >= 0: 
            k[i] =  np.log(k[i]/surface[i])
        else:
            k[i] = -np.log(abs(k[i])/surface[i])
    k = k/max(abs(k))
    färg = np.array([[i,1-i,0] for i in k])
    return färg, chai

#Beräknar laddning utifrån homogen fördelning
def homogeneous_ch(centroid,triangles,name):
    k = hct.charge_2(triangles, centroid, 5,name)
    chai = k
    arean = area_tri(triangles)
    print(sum([chai[i]*arean[i] for i in range(len(chai))]))
    for i in range(len(k)):
        if k[i] >= 0: 
            k[i] =  np.log(k[i])
        else:
            k[i] = -np.log(abs(k[i]))
    k = k/max(abs(k))
    färg = np.array([[0.5+0.5*i,0.5-0.5*i,0] for i in k])
    return färg,chai
    
    
def centroid(mesh,w):
    vertice = mesh.vertex["positions"].numpy()
    triangle = mesh.triangle["indices"].numpy()
    centroid = np.empty([len(triangle),3])
    extended = np.empty([3*len(triangle),3])
    for i in range (len(triangle)):
        h = np.asarray([vertice[int(triangle[i][0])],vertice[int(triangle[i][1])],vertice[int(triangle[i][2])]])
        t = [(h[0][j]+h[1][j]+h[2][j])/3 for j in range (3)]
        centroid[i] = t
        extended[3*i] = [(w*h[0][j]+h[1][j]+h[2][j])/(2+w) for j in range (3)]
        extended[3*i+1] = [(h[0][j]+w*h[1][j]+h[2][j])/(2+w) for j in range (3)]
        extended[3*i+2] = [(h[0][j]+h[1][j]+w*h[2][j])/(2+w) for j in range (3)]
    return centroid,vertice,triangle,extended

def area(vertice,triangle):
    surface = np.zeros(len(triangle))
    for i in range (len(triangle)):
        surface[i] = np.linalg.norm(np.cross(vertice[int(triangle[i][1])]-vertice[int(triangle[i][0])],vertice[int(triangle[i][2])]-vertice[int(triangle[i][0])]))/2
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


def potential_difference(triangles,charges,points):
    tot_pot= [0 for i in range(len(points))]
    for j in range(len(points)):
        for i in range(len(triangles)):
            tot_pot[j] = tot_pot[j] + hct.homogeneous_memo(triangles[i], points[j], i)*charges[i]
        print(tot_pot[j])
    return (tot_pot[1]-tot_pot[0])/np.linalg.norm(points[0]-points[1])      
            

def charge_difference(charges,laddningar):
    print(f'charges/laddningar = {(sum(charges))/(sum(laddningar))}')
    k = np.zeros(len(charges))
    for i in range(len(charges)):
        k[i] = abs(charges[i]-laddningar[i])/((charges[i]+laddningar[i])/2)*100
    return(sum(k)/len(k))        

##Kanske ändra till o3d.t 
mesh = o3d.geometry.TriangleMesh.create_box(3,3,3)
mesh = mesh.subdivide_midpoint(number_of_iterations= 3)
mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)




#print(mesh.vertex["positions"].numpy())

w= 5
center,vertice,triangle,extended = centroid(mesh,w)

#center_2,vertice_2,triangle_2,extended_2 = centroid(mesh2,w)
#print(len(center_2))
#center_3,vertice_3,triangle_3,extended_3 = centroid(mesh5,w)
#tot = np.concatenate((center,center_2,center_3))
triangles = get_triangles(vertice, triangle)
#triangles_2 = get_triangles(vertice_2, triangle_2)
#triangles_3 = get_triangles(vertice_3,triangle_3)
#tot_a = np.concatenate((triangles,triangles_2,triangles_3))
#tot_c = np.concatenate((extended,extended_2,extended_3))
#print(len(tot_a))

#Ändra från true eller false om man ska använda fler punkter eller inte
decision = 1


t = time.time()
färg,chai = point_ch(center,extended,triangles,decision)
#färg, chai = homogeneous_ch(extended, triangles,'box_charge_2')
#färg_2 = homogeneous_ch(tot,tot_a)
s = time.time()
print(s-t)
#c = np.zeros(len(a))
#for i in range(len(a)):
    #center_test,vertice_test,triangle_test,extended_test = centroid(mesh_test,a[i])
   # triangle_test = get_triangles(vertice_test, triangle_test)
  #  col,lad = point_ch(center_test,extended_test, triangle_test, 1)
 #   c[i] = sum(lad)

#print(b,c)
#print(potential_difference(tot_a,chai,punkter))
#mesh.triangle.colors = o3d.core.Tensor(färg[:len(center)],o3d.core.float32)
#mesh.compute_vertex_normals()


#mesh2.triangle.colors = o3d.core.Tensor(färg[len(center):len(center)+len(center_2)],o3d.core.float32)
#mesh2.compute_vertex_normals()


#mesh2.triangle.colors = o3d.core.Tensor(färg[len(center)+len(center_2):],o3d.core.float32)
#mesh2.compute_vertex_normals()


#o3d.visualization.draw([mesh,mesh2,mesh3])
