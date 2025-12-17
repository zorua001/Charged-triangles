# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 14:29:54 2025

@author: MSI Prestige
"""

import numpy as np 
import matplotlib.pyplot as plt

def mean(a,b):
    k = 0
    for i in range(len(a)):
        k = k + (a[i]-b[i])**2
    return np.sqrt(k/len(a))

triangles = [780,1200,2360,580,3160]

triangles_2 = [580,680,990,1680,2360]

time_homo = np.array([70.095,96.086,212.023,530.3876,964.05])

time_1 = np.array([9.59468,24.016,89.2366,5.2444,151.77])

time_2 = np.array([0.24532,0.544,5.4934,0.116,13.45])

triangles = sorted(triangles)

least = [(triangles[k]**3*3+triangles[k]**3+triangles[k]+triangles[k]**2*3)/(min(triangles)**3*3+min(triangles)**3 + min(triangles) + min(triangles)**2*3) for k in range(len(triangles))]

matrix = [triangles[k]**2*3/(min(triangles)**2*3) for k in range(len(triangles))]

matrix_homo = [triangles_2[k]**2.0/(min(triangles_2)**2.0) for k in range(len(triangles_2))]
matrix_homo_1 = [triangles_2[k]**1.8/(min(triangles_2)**1.8) for k in range(len(triangles_2))]
matrix_homo_2 = [triangles_2[k]**1.9/(min(triangles_2)**1.9) for k in range(len(triangles_2))]

print (matrix)

print(least)
time_2 = sorted(time_2)
time_1 = sorted(time_1)

#plt.plot(triangles,least,label='N^3')
#plt.plot(triangles,matrix,label='N^2')

k = np.log(triangles)
x = np.log(time_2/min(time_2))
coef = np.polyfit(k,x,1)
print(coef)
poly1d_fn = np.poly1d(coef)


plt.plot(k,x,'yo' ,label='Experimental')
plt.plot(k, poly1d_fn(k), '--k' ,label ='Linear fit')

plt.xlabel('No. Triangles')
plt.ylabel('Relative time')
plt.title('Complexity of least square')
#print('Mean square value for theoretical' , mean(least,time_2/min(time_2)))
#print('Mean square value for N^2' , mean(matrix,time_2/min(time_2)))

plt.legend()

plt.figure()

k = np.log(triangles)
x = np.log(time_1/min(time_1))
coef = np.polyfit(k,x,1)
print(coef)
poly1d_fn = np.poly1d(coef)

#plt.plot(triangles,matrix, label='Theoretical')
#plt.plot(np.log(triangles),np.log(time_1/min(time_1)),label='Experimental')
plt.plot(k,x,'yo' ,label='Experimental')
plt.plot(k, poly1d_fn(k), '--k' ,label ='Linear fit')

plt.xlabel('No. Triangles')
plt.ylabel('Relative time')
plt.title('Complexity of building matrix')
#print('Mean square value for point matrix' , mean(matrix,time_1/min(time_1)))
plt.legend()

plt.figure()


k = np.log(triangles_2)
x = np.log(time_homo/min(time_homo))
coef = np.polyfit(k,x,1)
print(coef)
poly1d_fn = np.poly1d(coef)

plt.plot(k,x,'yo' ,label='Experimental')
plt.plot(k, poly1d_fn(k), '--k' ,label ='Linear fit')

#plt.plot(triangles_2,matrix_homo, label='N^2')
#plt.plot(triangles_2,matrix_homo_2, label='N^1.9')
#plt.plot(triangles_2,matrix_homo_1, label='N^1.8')
#plt.plot(np.log(triangles_2),np.log(time_homo/min(time_homo)),label='Experimental')

#print('Mean square value for homogeneous N^2' , mean(matrix_homo,time_homo/min(time_homo)))
#print('Mean square value for homogeneous N^1.8' , mean(matrix_homo_1,time_homo/min(time_homo)))
#print('Mean square value for homogeneous N^1.9' , mean(matrix_homo_2,time_homo/min(time_homo)))

plt.xlabel('No. Triangles')
plt.ylabel('Relative time')
plt.title('Complexity of building matrix')
plt.legend()




