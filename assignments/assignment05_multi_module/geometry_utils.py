"""
DIGM 131 - Assignment 5: Multi-Module Toolkit (geometry_utils.py)
==================================================================

Geometry utility functions for creating and manipulating 3D primitives.

This module provides helper functions that wrap maya.cmds geometry creation
with sensible defaults, automatic naming, and ground-plane alignment.
"""

import maya.cmds as cmds


def create_box(name="box", width=1, height=1, depth=1, position=(0, 0, 0)):
    """Create a polygonal box with its base resting on the ground plane.

    Args:
        name (str): Desired name for the Maya transform node.
        width (float): Size along the X axis.
        height (float): Size along the Y axis.
        depth (float): Size along the Z axis.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of the created transform node.
    """
    # TODO: Implement -- create polyCube, move so base sits at y=0, return name.
    pass


def create_cylinder(name="cylinder", radius=0.5, height=2,
                    position=(0, 0, 0)):
    """Create a polygonal cylinder with its base resting on the ground plane.

    Args:
        name (str): Desired name for the Maya transform node.
        radius (float): Radius of the cylinder.
        height (float): Height of the cylinder.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of the created transform node.
    """
    # TODO: Implement.
    pass


def create_sphere(name="sphere", radius=1, position=(0, 0, 0)):
    """Create a polygonal sphere centered at the given position.

    Args:
        name (str): Desired name for the Maya transform node.
        radius (float): Radius of the sphere.
        position (tuple): (x, y, z) center position.

    Returns:
        str: The name of the created transform node.
    """
    # TODO: Implement.
    pass


def create_cone(name="cone", radius=1, height=2, position=(0, 0, 0)):
    """Create a polygonal cone with its base resting on the ground plane.

    Args:
        name (str): Desired name for the Maya transform node.
        radius (float): Base radius of the cone.
        height (float): Height of the cone.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of the created transform node.
    """
    # TODO: Implement.
    pass
