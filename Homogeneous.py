# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:44:27 2025

@author: MSI Prestige
"""

import numpy as np

def stora_p (a,b,c,d,e,n):
    return 2*np.log((b**2+d**2)*n+a*b+c*d+np.sqrt(((b**2+d**2)*n+a*b+c*d)**2+(a*d-b*c)**2+e**2*(b**2+d**2)))

def stora_q (a,b,c,d,e,n):
    t = d*e*((a*d-b*c)*(c+d*n)-b*e**2)
    number = np.arccos((abs(e*d)*np.sqrt((a+b*n)**2+(c+d*n)**2+e**2))/np.sqrt(((c+d*n)**2+e**2)*((a*d-b*c)**2+e**2*(b**2+d**2))))
    if t >= 0 :
        return - number
    return number

def stora_j (a,a_prim,b,b_prim,c,c_prim,d,e,n):
    k = a*d-b*c
    k_prim = a_prim*b_prim-b_prim*c_prim
    rad_1 = np.log((a+b*n + np.sqrt((a+b*n)**2+(c+d*n)**2+e**2))/(a_prim+b_prim*n+np.sqrt((a_prim+b_prim*n)**2+(c+d*n)**2+e**2)))*(c+d*n)/d 
    rad_2_1 = k*stora_p(a, b, c, d, e, n)/(2*d*np.sqrt(b**2+d**2))-k_prim*stora_p(a_prim, b_prim, c, d, e, n)/(2*d*np.sqrt(b_prim**2+d**2))
    rad_2_2 = (stora_q(a, b, c, d, e, n)-stora_q(a_prim, b_prim, c, d, e, n))*e/d
    return rad_1+rad_2_1+rad_2_2

def area (triange):
    return sum(abs(np.cross(triange[1]-triange[0],triange[2]-triange[0])))/2
    
    
def homogeneous (triange,point):
    alpha = sum([abs(triange[0][k]-triange[2][k])for k in range (3)])
    b_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[1]-triange[2]))/(alpha**2)
    a_prim = np.dot((triange[0]-triange[2]),np.transpose(triange[2]-point))/(alpha**2)
    a = 1 + a_prim
    b = b_prim -1
    q = sum(abs(np.cross(triange[0]-triange[2],triange[1]-triange[2])))
    n = np.cross(triange[0]-triange[2],triange[1]-triange[2])/q
    c = np.dot(n, np.transpose(np.cross(triange[0]-triange[2],triange[2]-point)))/(alpha**2)
    d = q/(alpha**2)
    e = abs(np.dot(n,np.transpose(triange[2]-point)))/alpha
    print(area(triange))
    c_prim = c ##Ingen aning vad c_prim är
    return (2*area(triange)/alpha)*(stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 1)-stora_j(a, a_prim, b, b_prim, c, c_prim, d, e, 0))


n = homogeneous(np.array([[0,0,0],[1,0,0],[0.25,1,0]]), np.array([2,2,2]))

print(n)