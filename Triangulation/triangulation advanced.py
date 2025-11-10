import numpy as np
import open3d as o3d

# Function to create a cylinder and extract triangle information
def create_cylinder_and_get_triangles(radius, height, num_sections):
    # Create a cylinder mesh
    cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius, height, z_direction=[0, 0, 1], resolution=num_sections)
    cylinder.compute_vertex_normals()  # Optional: compute normals for better visualization
    
    # Extract triangle vertices
    triangles = np.asarray(cylinder.triangles)  # Get triangles as indices
    vertices = np.asarray(cylinder.vertices)    # Get vertex coordinates

    # Get triangle vertex coordinates and calculate triangle centers
    triangle_vertices = []
    triangle_centers = []
    
    for tri in triangles:
        # Get the coordinates of the triangle vertices
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        
        triangle_vertices.append([v1, v2, v3])
        
        # Calculate the center of the triangle
        center = (v1 + v2 + v3) / 3.0
        triangle_centers.append(center)
    
    return triangle_vertices, triangle_centers

# Parameters for the cylinder
radius = 1.0
height = 2.0
num_sections = 20

# Create cylinder and extract triangle information
triangle_vertices, triangle_centers = create_cylinder_and_get_triangles(radius, height, num_sections)

# Print triangle vertices and their centers
for i, (vertices, center) in enumerate(zip(triangle_vertices, triangle_centers)):
    print(f"Triangle {i} Vertices:\n {vertices[0]}, \n {vertices[1]}, \n {vertices[2]}")
    print(f"Triangle {i} Center: {center}\n")
