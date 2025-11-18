# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 11:47:38 2025

@author: MSI Prestige
"""
import numpy as np

def stora_F (p,q,n):
    x_1 = n*np.arcsinh(((p*n+q)/np.sqrt(n**2+1)))
    x_2 = q*np.log((((p**2+1)*n+p*q)/np.sqrt(p**2+q**2+1))+np.sqrt((((p**2+1)*n+p*q)/np.sqrt(p**2+q**2+1))**2+1))/np.sqrt(p**2+1)
    x_3 = np.arctan((q*n-p)/np.sqrt((p*n+q)**2+n**2+1))
    return x_1+x_2-x_3

def area (triange):
    temp = abs(np.cross(triange[1]-triange[0],triange[2]-triange[0]))
    m = 0
    for i in temp:
        m = m+i**2
    return m**0.5/2
    
def barycentric (vertex,point):
    s = area(vertex)
    k = [np.cross((vertex[i%3][:2]-point[:2]),(vertex[(i+1)%3][:2]-point[:2]))/(2*s) for i in range (3)]
    k.append(abs(point[2]))
    print(k)
    return k

def barycentric_2 (vertex,point):
    p_prim = [point[0],point[1],0]
    print(p_prim)
    k = [np.cross(vertex[(i+1)%3],vertex[(i+2)%3])-np.cross(p_prim,(vertex[(i+2)%3]-vertex[(i+1)%3])) for i in range (3)]/(2*area(vertex))
    k = np.dot(k,[0,0,1])
    k = np.append(k,point[2])
    print(k)
    return k
    
    
def distance(vertex):
    return [sum((vertex[(i+2)%3]-vertex[(i+1)%3])**2)**0.5 for i in range (3)]

def variables(dist,bary,size):
    p_1 = (dist[0]**2+dist[1]**2-dist[2]**2)*4*size
    p_2 = -(dist[2]**2+dist[0]**2-dist[1]**2)*4*size
    n_1 = - bary[0]/(8*size*dist[0]*bary[3])
    n_2 = ( 1 - bary[0])/(8*size*dist[0]*bary[3])
    q_1 = -dist[0]*bary[1]/bary[3]
    q_2 =  dist[0]*bary[2]/bary[3]
    return [p_1,p_2,q_1,q_2,n_1,n_2]

def potential(variable,size,bary):
    # bestäm laddning
    Q = 1
    e_0 = 8.854*10**(-12)
    t = Q*bary[3]*8*size/(2*np.pi*e_0) *(stora_F(variable[1], variable[3], variable[5])-stora_F(variable[1], variable[3], variable[4])-stora_F(variable[0], variable[2], variable[5])+stora_F(variable[0], variable[2], variable[4]))
    return t*4*np.pi*e_0*size/Q
    
vertex = np.array([[0,0,0],[1,0,0],[0.25,1,0]])
bary = barycentric_2(vertex, np.array([2,2,2]))
dist = distance(vertex)
variable = variables(dist,bary,area(vertex))

print(variable)
print(potential(variable, area(vertex), bary))