"""
DIGM 131 - Assignment 5: Multi-Module Toolkit (layout_utils.py)
================================================================

Layout utility functions for arranging objects in common spatial patterns.

This module provides functions to position existing or newly-created
objects in lines, grids, and circles.
"""

import math
import maya.cmds as cmds


def arrange_in_line(objects, start=(0, 0, 0), spacing=3.0, axis="x"):
    """Move a list of existing objects into a straight line.

    Args:
        objects (list): List of Maya transform node names to reposition.
        start (tuple): (x, y, z) position of the first object.
        spacing (float): Distance between each object along the chosen axis.
        axis (str): The axis along which to space objects. One of
            "x", "y", or "z".

    Returns:
        None
    """
    # TODO: Implement.
    #   1. Loop through 'objects' with enumerate to get an index.
    #   2. Calculate the position offset: index * spacing.
    #   3. Build (x, y, z) based on which axis is selected.
    #   4. cmds.move(x, y, z, obj)
    pass


def arrange_in_grid(objects, rows=3, cols=3, spacing=3.0, origin=(0, 0, 0)):
    """Arrange a list of objects into a grid on the XZ plane.

    If len(objects) < rows * cols, only the available objects are placed.
    Extra grid positions are left empty.

    Args:
        objects (list): List of Maya transform node names.
        rows (int): Number of rows (Z direction).
        cols (int): Number of columns (X direction).
        spacing (float): Distance between adjacent grid cells.
        origin (tuple): (x, y, z) position of the first cell (row 0, col 0).

    Returns:
        None
    """
    # TODO: Implement.
    #   1. Use a counter or enumerate to track which object you are placing.
    #   2. Nested loop over rows and cols.
    #   3. Calculate x and z from col * spacing and row * spacing.
    #   4. Move the next object to that position.
    pass


def arrange_in_circle(objects, radius=10, center=(0, 0, 0)):
    """Arrange existing objects evenly around a circle on the XZ plane.

    Args:
        objects (list): List of Maya transform node names.
        radius (float): Radius of the circle.
        center (tuple): (x, y, z) center of the circle.

    Returns:
        None
    """
    # TODO: Implement.
    #   1. Calculate the angle step: 2 * math.pi / len(objects).
    #   2. Loop through objects with enumerate.
    #   3. x = center[0] + radius * math.cos(angle)
    #      z = center[2] + radius * math.sin(angle)
    #   4. cmds.move(x, center[1], z, obj)
    pass
