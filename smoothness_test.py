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
from charge.calculate_potential import calculate_potential


def plot_circle(angles,potentials, radius):
    # Plot the points using Matplotlib
    plt.figure(figsize=(8, 8))
    plt.scatter(angles, potentials, marker='o')
    plt.title(f'Potential at radius {radius}')
    plt.xlabel('Angle (radians)')
    plt.ylabel('Potential')
    plt.axis('auto')  # Equal aspect ratio
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

'''
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

'''
'''
def plot_triangle_and_potential(v1, v2, v3, points, potentials):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Adjust z-axis scaling to make height scaling faster
    ax.set_box_aspect([1, 1, 0.5])  # Aspect ratio

    # Create a triangulation for the topography
    # If you want to adjust visualization speeds here, consider modifying potential or z dimensions
    # Avoid plotting the triangle edges
    # Triangle vertices
    triangle_vertices = np.array([v1, v2, v3])
    # Create a surface plot instead of line plot to enhance visualization
    ax.plot_trisurf(triangle_vertices[:, 0], triangle_vertices[:, 1], triangle_vertices[:, 2], 
                    color='lightgrey', alpha=0.1, antialiased=True)

    # Plot points with a color map based on their z-values
    sc = ax.scatter(points[:, 0], points[:, 1], potentials, c=potentials, cmap='viridis', label='Potential')

    # Labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Potential (Height)')
    ax.set_title('Surface Triangle with Potential Map')
    ax.legend()

    # Add a color bar
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('Potential')

    plt.show()
    
    '''
'''
def rotate_and_plot_triangle(v1, v2, v3, points, potentials):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Adjust z-axis scaling to make height scaling faster
    ax.set_box_aspect([1, 1, 0.5])  # Aspect ratio

    # Create triangle vertices
    triangle_vertices = np.array([v1, v2, v3])
    
    # Calculate centroid for rotation around the centroid
    centroid = np.mean(triangle_vertices, axis=0)

    # Create a rotation matrix (example: 90 degrees around the z-axis)
    theta = np.pi / 2  # 90 degrees in radians
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                 [np.sin(theta), np.cos(theta), 0],
                                 [0, 0, 1]])

    # Rotate triangle vertices and translate to the centroid
    rotated_vertices = (triangle_vertices - centroid) @ rotation_matrix + centroid

    # Plot the rotated triangle
    ax.plot_trisurf(rotated_vertices[:, 0], rotated_vertices[:, 1], 
                     rotated_vertices[:, 2], color='lightgrey', alpha=0.1, antialiased=True)

    # Plot points with a color map based on their z-values
    sc = ax.scatter(points[:, 0], points[:, 1], potentials, c=potentials, cmap='viridis', label='Potential')

    # Labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Potential (Height)')
    ax.set_title('Rotated Triangle with Potential Map')
    ax.legend()

    # Add a color bar
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('Potential')

    plt.axis('equal')  # Maintain equal scaling on both axes
    plt.grid(True)
    plt.show()
    
    '''
    
    
def rotate_to_xy(vertices, points):
    def compute_normal(v1, v2, v3):
        edge1 = v2 - v1
        edge2 = v3 - v1
        return np.cross(edge1, edge2)

    # Calculate the normal of the triangle formed by the vertices
    normal = compute_normal(vertices[0], vertices[1], vertices[2])
    normal = normal / np.linalg.norm(normal)  # Normalize the normal vector

    # Define the target normal vector (Z-axis)
    target_normal = np.array([0, 0, 1])

    # Calculate the rotation axis and angle
    rotation_axis = np.cross(normal, target_normal)
    rotation_angle = np.arccos(np.clip(np.dot(normal, target_normal), -1.0, 1.0))

    # Create the rotation matrix using Rodrigues' rotation formula
    if np.linalg.norm(rotation_axis) != 0:  # Check if a rotation is needed
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        K = np.array([[0, -rotation_axis[2], rotation_axis[1]],
                      [rotation_axis[2], 0, -rotation_axis[0]],
                      [-rotation_axis[1], rotation_axis[0], 0]])
        R = np.eye(3) + np.sin(rotation_angle) * K + (1 - np.cos(rotation_angle)) * K @ K
    else:
        R = np.eye(3)  # No rotation needed if already aligned
    
    # Rotate triangle vertices
    rotated_vertices = vertices @ R.T
    
    # Rotate points
    rotated_points = points @ R.T
    
    return rotated_vertices, rotated_points 


def rotate_and_translate_to_xy(vertices, points):
    def compute_normal(v1, v2, v3):
        edge1 = v2 - v1
        edge2 = v3 - v1
        return np.cross(edge1, edge2)

    # Calculate the normal of the triangle formed by the vertices
    normal = compute_normal(vertices[0], vertices[1], vertices[2])
    normal = normal / np.linalg.norm(normal)  # Normalize the normal vector

    # Define the target normal vector (Z-axis)
    target_normal = np.array([0, 0, 1])

    # Calculate the rotation axis and angle
    rotation_axis = np.cross(normal, target_normal)
    rotation_angle = np.arccos(np.clip(np.dot(normal, target_normal), -1.0, 1.0))

    # Create the rotation matrix using Rodrigues' rotation formula
    if np.linalg.norm(rotation_axis) != 0:  # Check if a rotation is needed
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        K = np.array([[0, -rotation_axis[2], rotation_axis[1]],
                      [rotation_axis[2], 0, -rotation_axis[0]],
                      [-rotation_axis[1], rotation_axis[0], 0]])
        R = np.eye(3) + np.sin(rotation_angle) * K + (1 - np.cos(rotation_angle)) * K @ K
    else:
        R = np.eye(3)  # No rotation needed if already aligned

    # Rotate triangle vertices
    rotated_vertices = vertices @ R.T
    
    # Rotate points
    rotated_points = points @ R.T
    
    # Calculate the centroid of the original triangle
    centroid = np.mean(rotated_vertices, axis=0)
    
    # Translate both vertices and points to move the centroid to (0, 0, 0)
    translated_vertices = rotated_vertices - centroid
    translated_points = rotated_points - centroid

    return translated_vertices, translated_points

def plot_centered_triangle(v1, v2, v3, points, potentials, std_dev,mean,r_squared):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create triangle vertices
    triangle_vertices = np.array([v1, v2, v3])

    # Calculate centroid
    centroid = np.mean(triangle_vertices, axis=0)

    # Center the triangle at the origin by translating vertices
    centered_vertices = triangle_vertices - centroid

    # Create a surface plot for the centered triangle
    #ax.plot_trisurf(centered_vertices[:, 0], centered_vertices[:, 1], 
    #                 centered_vertices[:, 2], color='lightgrey', alpha=0.5, antialiased=True)

    # Plot points with a color map based on their z-values
    sc = ax.scatter(points[:, 0], points[:, 1], potentials, c=potentials, cmap='viridis', label='Potential')

    # Display unrelated values as annotations

    ax.text2D(0.5, -0.10, f'Standard Deviation: {std_dev:.2e}', 
          horizontalalignment='center', verticalalignment='bottom', 
          transform=ax.transAxes, fontsize=8)
    ax.text2D(0.5, -0.14, f'Mean: {mean:.2e}', 
          horizontalalignment='center', verticalalignment='bottom', 
          transform=ax.transAxes, fontsize=8)
    ax.text2D(0.5, -0.18, f'R²: {r_squared:.2e}', 
          horizontalalignment='center', verticalalignment='bottom', 
          transform=ax.transAxes, fontsize=8)
    # Labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Potential (Height)')
    ax.set_title('Centered Triangle with Potential Map')
    ax.legend()

    # Add a color bar
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('Potential')

    # Maintain aspect ratio and grid
    ax.set_box_aspect([1, 1, 0.5])  # Often used for better visual scaling
    
   
    
    plt.show()
  


def run_test(simulation_params, visualization_params):
    #Setup
    #Already done through loading the save
    print(f'Simulation parameters: {simulation_params}')
    
    method = simulation_params['charge_distribution_method']
    
    bodies = simulation_params['bodies']
    
    charges = [] 
    for body in bodies:
        s_charges=body.charges 
        charges.extend(s_charges)
    
    triangles = []
    for body in bodies:
        if(method=='homogenous'):
            s_triangle = body.get_triangle_vertices()
        else:
            s_triangle = body.get_centroids()
        
        triangles.append(s_triangle) 
    
    triangles = np.vstack((triangles) if triangles else np.array([]))
    
    '''Circle test'''
    '''
    #We decide on some radii and center (these are based on a cylinder radius of 10)
    radii = [1,1.1,1.2,1.3,3,10,20]
    center = (0,0,0)
    resolution = 100
    total_points = []
    for radius in radii:
        points,angles = generate_circle_points_in_xy_plane(resolution, radius, center)
        total_points.append(points)
        potentials = [calculate_potential(triangles,charges, point, method) for point in points]
        plot_circle(angles,potentials,radius)
       
    '''

    '''Full triangle test'''
    index = 200
    resolution = 1000
    triangle_vertices = bodies[0].get_triangle_vertices()[index]
    points = generate_evenly_distributed_points(triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], resolution)
    potentials = [calculate_potential(triangles,charges,p,method) for p in points]
    #Calculates standard deviation, mean and error
    # Calculate standard deviation
    std_dev = np.std(potentials)
    mean = np.mean(potentials)
    SS_tot = np.sum((potentials - mean) ** 2)  # Total sum of squares
    SS_res = np.sum((potentials - np.polyval(np.polyfit(range(len(potentials)), potentials, 1), range(len(potentials)))) ** 2)  # Residual sum of squares
    r_squared = 1 - (SS_res / SS_tot)
    #rotate triangle to x-y plane:
    rot_vert, rot_points = rotate_and_translate_to_xy(triangle_vertices,points)
    #Plot everything     
    plot_centered_triangle(rot_vert[0], rot_vert[1], rot_vert[2], rot_points, potentials,std_dev,mean,r_squared)
    
    
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