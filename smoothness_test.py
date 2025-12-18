# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 11:15:01 2025

@author: Hampus Berndt
"""

import argparse
import open3d as o3d
import numpy as np
from config.load_save import load_save
from config.settings_loader import load_visualization_settings
from config.allowed_bodies import Body
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from charge.calculate_potential import calculate_potential_from_point


def plot_circle(angles,potentials, radius):
    # Plot the points using Matplotlib
    plt.figure(figsize=(8, 8))
    plt.scatter(angles, potentials, marker='o')
    plt.title(f'Potential at radius {radius}')
    plt.xlabel('Angle (radians)')
    plt.ylabel('Potential')
    plt.axis('equal')  # Equal aspect ratio
    plt.grid(True)
    plt.show()



def generate_circle_points_in_xy_plane(amount, radius, center=(0, 0, 0)):
    # Calculate the angle between each point
    angles = np.linspace(0, 2 * np.pi, amount, endpoint=False)
    
    # Calculate the coordinates with specified center
    points = [
        (center[0] + radius * np.cos(angle), 
         center[1] + radius * np.sin(angle), 
         center[2]) for angle in angles
    ]
    
    return points,angles


def generate_evenly_distributed_points(v1, v2, v3, num_points):
    # Calculate the total area of the triangle
    def area(v1, v2, v3):
        return np.linalg.norm(np.cross(v2 - v1, v3 - v1)) / 2

    # Number of points can be a square root of the area for even distribution
    total_area = area(v1, v2, v3)
    
    # Calculate the number of points along each edge
    points_per_side = int(np.sqrt(num_points * (total_area / (total_area * 2))))

    points = []
    
    # Iterate over a grid within the triangle
    for i in range(points_per_side + 1):
        for j in range(points_per_side + 1 - i):  # to ensure inside the triangle
            # Compute barycentric coordinates
            r1 = i / points_per_side
            r2 = j / points_per_side
            
            # Get the point coordinates
            point = (1 - r1 - r2) * v1 + r1 * v2 + r2 * v3
            points.append(point)

    return np.array(points)

def plot_triangle_and_potential(v1, v2, v3, points, potentials):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the triangle edges
    triangle = np.array([v1, v2, v3, v1])
    ax.plot(triangle[:, 0], triangle[:, 1], triangle[:, 2], color='b', label='Triangle Edges')


    # Plot points with a color map based on their z-values
    sc = ax.scatter(points[:, 0], points[:, 1], potentials, c=potentials, cmap='viridis', label='Topography')

    # Labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Potential (Height)')
    ax.set_title('Surfacetriangle with Potential Map')
    ax.legend()

    # Add a color bar
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('Potential')

    plt.show()



def run_test(simulation_params, visualization_params):
    #Setup
    #Already done through loading the save
    print(f'Simulation parameters: {simulation_params}')
    
    bodies = simulation_params['bodies']
    
    '''Circle test'''
   
    #We decide on some radii and center (these are based on a cylinder radius of 10)
    radii = [1,1.1,1.2,1.3,3,10,20]
    center = (0,0,0)
    resolution = 1000
    total_points = []
    for radius in radii:
        points,angles = generate_circle_points_in_xy_plane(resolution, radius, center)
        total_points.append(points)
        potentials = [calculate_potential_from_point(point) for point in points]
        plot_circle(angles,potentials,radius)
       


    '''Full triangle test'''
    index = 1
    resolution = 1000
    triangle_vertices = bodies[0].get_triangle_vertices()[index]
    points = generate_evenly_distributed_points(triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], resolution)
    potentials = [calculate_potential_from_point(p) for p in points]
    plot_triangle_and_potential(triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], points, potentials)
    
    '''Random scatter test'''
    
    
    
    #Visualize everything
    #We create the colors in the bodies.
        #We then visualize all the bodies
    #for body in simulation_params['bodies']:
    #    body.calculate_colors(simulation_params['charge_distribution_method'], visualization_params['color_method'])
        
    #o3d.visualization.draw([body for body in bodies])
 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the results of a previous simulation.")
    parser.add_argument("--save", type=str, default = 'hvp_smoothness_p_cylinder_400_1', help="Name of the save file to use. The save files can be found under the saves directory")
    parser.add_argument("--visualization", type=str, default="settings_default", help="Name of the visualization settings file to use.")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_arguments()
    simulation_params = load_save(args.save)
    visualization_params = load_visualization_settings(args.visualization)
    run_test(simulation_params, visualization_params)