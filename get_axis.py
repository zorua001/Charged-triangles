# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 11:43:05 2025

@author: Hampus Berndt
"""
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

def get_axis(length):
    axis = o3d.geometry.LineSet()
    axis.points = o3d.utility.Vector3dVector([[0, 0, 0], [length, 0, 0], [0, length, 0], [0, 0, length]])
    axis.lines = o3d.utility.Vector2iVector([[0, 1], [0, 2], [0, 3]])
    #axis.colors = o3d.utility.Vector3dVector([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # RGB colors
    # Create ticks
    ticks = o3d.geometry.LineSet()
    tick_points = []
    tick_length = 0.1
    
    # Add X ticks
    for i in range(1, int(length) + 1):
        tick_points.append([i, 0, 0])
        tick_points.append([i, tick_length, 0])
    
    # Add Y ticks
    for i in range(1, int(length) + 1):
        tick_points.append([0, i, 0])
        tick_points.append([tick_length, i, 0])
    
    # Add Z ticks
    for i in range(1, int(length) + 1):
        tick_points.append([0, 0, i])
        tick_points.append([0, tick_length, i])
    
    ticks.points = o3d.utility.Vector3dVector(tick_points)
    tick_lines = np.array([[2 * i, 2 * i + 1] for i in range(len(tick_points) // 2)])
    ticks.lines = o3d.utility.Vector2iVector(tick_lines)
    ticks.colors = o3d.utility.Vector3dVector([[0, 0, 0]] * len(tick_lines))  # Black color for ticks
    
    return axis, ticks


def create_color_scale(min_value, max_value, num_colors=10):
    # Interpolate colors from red to green
    colors = []
    for i in range(num_colors):
        ratio = i / (num_colors - 1)
        color = [1 - ratio, ratio, 0]  # From [1, 0, 0] to [0, 1, 0]
        colors.append(color)

    # Create the color scale plot using Matplotlib
    plt.figure(figsize=(2, num_colors))
    for i in range(num_colors):
        plt.fill_betweenx([i, i + 1], 0, 1, color=colors[i])

    # Set ticks to show values
    ticks = np.linspace(min_value, max_value, num_colors)
    plt.yticks(np.arange(num_colors) + 0.5, [f"{val:.2f}" for val in ticks])
    plt.xticks([])
    plt.title("Color Scale")
    plt.show()