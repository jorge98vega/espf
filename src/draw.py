# Imports

import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import unary_union

# Functions


def intersection_circle(center, radius, dim=0, plane=0):
    """
    Computes the intersection of a sphere with a plane defined by dim = plane.
    
    Args:
        center (tuple): The center of the sphere (x, y, z).
        radius (float): The radius of the sphere.
        dim (int): The dimension of the plane (0 = x, 1 = y, 2 = z).
        plane (float): The coordinate value of the plane.
    
    Returns:
        shapely.geometry.Polygon or None: The intersection circle as a 2D geometry
        (or None if there is no intersection).
    """
    d = abs(center[dim] - plane) # Distance from the sphere center to the plane
    r2 = radius**2 - d**2 # Radius squared of the intersection circle
    if r2 < 0:
        return None # No intersection
    
    center2d = np.delete(center, dim) # Center of the circle in the plane (remove the plane dimension)
    return Point(center2d[0], center2d[1]).buffer(np.sqrt(r2)) # Return a 2D circle as a Shapely Polygon


def plot_sphere_intersections(spheres, dim=0, plane=0, ax=None):
    """
    Plots the intersections of multiple spheres in the plane defined by dim = plane,
    excluding internal overlaps. Can overlay the circles on an existing matplotlib axis.

    Args:
        spheres (list): List of tuples, each containing (center, radius).
        dim (int): The dimension of the plane (0 = x, 1 = y, 2 = z).
        plane (float): The coordinate value of the plane.
        ax (matplotlib.axes._subplots.AxesSubplot, optional): Existing axis to plot on.
    """
    # Calculate intersections of all spheres with the plane
    circles = []
    for center, radius in spheres:
        circle = intersection_circle(center, radius, dim, plane)
        if circle:
            circles.append(circle)

    # Handle the case where there are no intersections
    if len(circles) == 0:
        print("No intersections for this plane.")
        return

    # Combine all circles
    combined_shape = unary_union(circles)
    # Check if the combined shape is a Polygon or MultiPolygon
    if isinstance(combined_shape, Polygon):
        combined_shape = [combined_shape]  # Wrap single polygon into a list
    elif isinstance(combined_shape, MultiPolygon):
        combined_shape = list(combined_shape.geoms)  # Extract individual geometries

    # Create a new axis with the default labels and title if none is provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        labels = ['x', 'y', 'z']
        ax.set_xlabel(labels[np.delete([0, 1, 2], dim)[0]])
        ax.set_ylabel(labels[np.delete([0, 1, 2], dim)[1]])
        ax.set_title(f'Intersection of spheres in the {["x", "y", "z"][dim]} = {plane} plane')

    # Iterate and plot each geometry
    for poly in combined_shape:
        x, y = poly.exterior.xy
        ax.plot(x, y, linewidth=2, linestyle='--', color='k')

    # Ensure aspect ratio is equal
    ax.set_aspect('equal', adjustable='box')