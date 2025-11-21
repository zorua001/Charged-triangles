# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:44:27 2025

@author: MSI Prestige
"""

import numpy as np
import functools
import concurrent.futures as future

def stora_p (a,b,c,d,e,n):
    return 2*np.log((b**2+d**2)*n+a*b+c*d+np.sqrt(((b**2+d**2)*n+a*b+c*d)**2+(a*d-b*c)**2+e**2*(b**2+d**2)))

def stora_q (a,b,c,d,e,n):
    t = d*e*((a*d-b*c)*(c+d*n)-b*e**2)
    x =(abs(e*d)*np.sqrt((a+b*n)**2+(c+d*n)**2+e**2))/np.sqrt(((c+d*n)**2+e**2)*((a*d-b*c)**2+(e**2)*(b**2+d**2)))
    if np.isnan(x):
        x = 0
    if abs(x) <= 1:
        number = np.arccos(x)
    else: 
        number = np.arccos(1)
    if t >= 0 :
        return - number
    return number

def stora_j (a,a_prim,b,b_prim,c,c_prim,d,e,n):
    k = a*d-b*c
    k_prim = a_prim*d-b_prim*c ## Försöker använda formeln för k från linär 
    rad_1 = np.log((a+b*n + np.sqrt((a+b*n)**2+(c+d*n)**2+e**2))/(a_prim+b_prim*n+np.sqrt((a_prim+b_prim*n)**2+(c+d*n)**2+e**2)))*(c+d*n)/d 
    rad_2_1 = k*stora_p(a, b, c, d, e, n)/(2*d*np.sqrt(b**2+d**2))-k_prim*stora_p(a_prim, b_prim, c, d, e, n)/(2*d*np.sqrt(b_prim**2+d**2))
    rad_2_2 = (stora_q(a, b, c, d, e, n)-stora_q(a_prim, b_prim, c, d, e, n))*e/d
    return rad_1+rad_2_1+rad_2_2

def area (triange):
    temp = abs(np.cross(triange[1]-triange[0],triange[2]-triange[0]))
    m = 0
    for i in temp:
        m = m+i**2
    return m**0.5/2
    
    
def homogeneous (triange,point):
    alpha = np.linalg.norm(triange[0]-triange[2])
    b_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[1]-triange[2]))/(alpha**2)
    a_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[2]-point))/(alpha**2)
    a = 1 + a_prim
    b = b_prim -1
    q_t = abs(np.cross(triange[0]-triange[2],triange[1]-triange[2]))
    q = sum([q_t[k]**2 for k in range (3)])**0.5
    n = np.cross(triange[0]-triange[2],triange[1]-triange[2])/q
    c = np.dot(n, np.transpose(np.cross(triange[0]-triange[2],triange[2]-point)))/(alpha**2)
    d = q/(alpha**2)
    e = abs(np.dot(n,np.transpose(triange[2]-point)))/alpha
    c_prim = c ##Ingen aning vad c_prim är
    return (2*area(triange)/alpha)*(stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 1)-stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 0))

def homogeneous_memo (triange,point,j):
    if j in memory:
        alpha = memory[j][0]
        b_prim = memory[j][1]
        n = memory[j][2]
        d = memory[j][3]
    else:     
        alpha = np.linalg.norm(triange[0]-triange[2])
        b_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[1]-triange[2]))/(alpha**2)
        q_t = abs(np.cross(triange[0]-triange[2],triange[1]-triange[2]))
        q = sum([q_t[k]**2 for k in range (3)])**0.5
        n = np.cross(triange[0]-triange[2],triange[1]-triange[2])/q
        d = q/(alpha**2)
        memory[j] = [alpha,b_prim,n,d]
    a_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[2]-point))/(alpha**2)
    a = 1 + a_prim
    b = b_prim -1
    
    c = np.dot(n, np.transpose(np.cross(triange[0]-triange[2],triange[2]-point)))/(alpha**2)
   
    e = abs(np.dot(n,np.transpose(triange[2]-point)))/alpha
    c_prim = c ##Ingen aning vad c_prim är
    return (2*area(triange)/alpha)*(stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 1)-stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 0))


#Kopierade från Parallell_charges
def charge(vertex_coordinates,points,potentia):
    print("hello")
    distance = np.zeros([len(vertex_coordinates),len(points)])
    for i in range (len(vertex_coordinates)):
        k = functools.partial(homogeneous_memo,vertex_coordinates[i])
        with future.ThreadPoolExecutor() as executor:
            distance[i] = list(executor.map(k, points))
        print("k")
    distance[np.isnan(distance)] = 0
    distance[np.isinf(distance)] = 0
    potentia = np.ones(len(points))*potentia
    print("hej")
    t = np.linalg.lstsq(distance.astype('float') , potentia.astype('float'),rcond=-1)[0]
    return t

def charge_2(vertex_coordinates,points,potentia):
    print("hello")
    distance = np.zeros([len(points),len(vertex_coordinates)])
    for j in range(len(vertex_coordinates)):
        for i in range(len(points)):
            distance[i,j] = homogeneous_memo(vertex_coordinates[j], points[i],j)
        print("k")
    distance[np.isnan(distance)] = 0
    distance[np.isinf(distance)] = 0
    potentia = np.ones(len(points))*potentia
    print("hej")
    t = np.linalg.lstsq(distance.astype('float') , potentia.astype('float'),rcond=-1)[0]
    return t


memory = {}
#n = homogeneous(np.array([[1,0,0],[0.5,0.867,0],[0,0,0]]), np.array([0.5,0.289,0.5]))
#m = homogeneous(np.array([[0,0,0],[1,0,0], [0.25,1,0]]), np.array([2,0,2]))

#print(n)
#print(m)