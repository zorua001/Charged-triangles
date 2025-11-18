# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 16:10:24 2025

@author: Hampus Berndt
"""
import open3d as o3d

mesh1 = o3d.t.geometry.TriangleMesh.create_cylinder(1,8,10,10)
mesh2 = o3d.t.geometry.TriangleMesh.create_sphere(3).translate([4,0,0])
mesh1.vertices
o3d.visualization.draw([mesh1,mesh2])