"""
Assignment 7: Simple Class-Based Scene Tool
DIGM 131 - Intro to Scripting for Digital Media

OBJECTIVE:
    Use Python classes to represent objects in a Maya scene. Each class
    encapsulates the data and behavior for one type of scene element.

REQUIREMENTS:
    1. Complete the Building and Tree classes below
    2. Each class must create actual Maya geometry in __init__ or in a build() method
    3. Each class must store the names of created Maya objects so they can be
       modified or deleted later
    4. Use PascalCase for class names, snake_case for methods and variables
    5. All methods must have docstrings
    6. Add at least ONE additional method to each class beyond what is provided

CONCEPTS PRACTICED:
    - Classes and objects (OOP basics)
    - __init__ (constructor)
    - self and instance variables
    - Methods that operate on object data
    - Encapsulation: grouping related data and behavior

DELIVERABLES:
    - This file with both classes completed
    - main.py with a scene built using your classes

NOTES:
    - A class is a blueprint. An instance is a specific object built from that blueprint.
    - 'self' refers to the specific instance. self.height is THAT building's height.
    - Think of __init__ as the setup instructions that run when you create a new instance.
"""

import maya.cmds as cmds


class Building(object):
    """Represents a simple building made of Maya geometry.

    A Building consists of a base (cube) and optional features like
    windows or a rooftop structure. The class stores references to all
    created Maya objects so they can be moved, modified, or deleted.

    Attributes:
        name (str): Base name for the building.
        width (float): Width of the building (X axis).
        height (float): Height of the building (Y axis).
        depth (float): Depth of the building (Z axis).
        parts (list): Names of all Maya objects that make up this building.
    """

    def __init__(self, name, width=2.0, height=5.0, depth=2.0):
        """Initialize a Building and create its base geometry in Maya.

        Args:
            name (str): Base name for the building.
            width (float): Width of the building.
            height (float): Height of the building.
            depth (float): Depth of the building.
        """
        # TODO: Store the parameters as instance variables (self.name, etc.)

        # TODO: Initialize self.parts as an empty list

        # TODO: Create the main body of the building using cmds.polyCube()
        #   - Set the dimensions to width, height, depth
        #   - Move it so the base sits on the ground plane (Y = height / 2)
        #   - Append the cube's name to self.parts

        pass

    def add_windows(self, rows=3, columns=2):
        """Add window-like cubes to the front face of the building.

        Windows should be small cubes positioned on the front face of the
        building, evenly spaced based on rows and columns.

        Args:
            rows (int): Number of rows of windows.
            columns (int): Number of columns of windows.

        Returns:
            list: Names of the created window objects.
        """
        # TODO: Calculate spacing based on self.height, self.width, rows, columns

        # TODO: Use nested loops to create small cubes for each window
        #   - Position each window on the front face of the building
        #   - Name them systematically (e.g., "myBuilding_window_0_0")
        #   - Append each to self.parts

        # TODO: Return the list of window names

        pass

    def move(self, x, y, z):
        """Move the entire building (all parts) to a new position.

        Args:
            x (float): X position.
            y (float): Y position.
            z (float): Z position.
        """
        # TODO: Loop through self.parts and move each one
        #   Hint: You may want to group them first, or move each individually
        #   Consider using cmds.group() in __init__ to make this simpler

        pass

    # TODO: Add at least ONE more method of your choice. Ideas:
    #   - set_color(self, color_index): Change the building's wireframe color
    #   - delete(self): Remove all parts from the scene
    #   - add_roof(self): Add a roof shape on top
    #   - scale(self, factor): Scale the building uniformly


class Tree(object):
    """Represents a simple tree made of Maya geometry.

    A Tree consists of a trunk (cylinder) and a canopy (sphere). The class
    stores references to created Maya objects.

    Attributes:
        name (str): Base name for the tree.
        trunk_height (float): Height of the trunk.
        canopy_radius (float): Radius of the canopy sphere.
        parts (list): Names of all Maya objects that make up this tree.
    """

    def __init__(self, name, trunk_height=3.0, canopy_radius=1.5):
        """Initialize a Tree and create its geometry in Maya.

        Args:
            name (str): Base name for the tree.
            trunk_height (float): Height of the tree trunk.
            canopy_radius (float): Radius of the canopy.
        """
        # TODO: Store parameters as instance variables

        # TODO: Initialize self.parts as an empty list

        # TODO: Create the trunk using cmds.polyCylinder()
        #   - Set height to trunk_height, radius to something small (e.g., 0.3)
        #   - Move it so the base sits on the ground (Y = trunk_height / 2)
        #   - Append to self.parts

        # TODO: Create the canopy using cmds.polySphere()
        #   - Set radius to canopy_radius
        #   - Position it on top of the trunk (Y = trunk_height + canopy_radius * 0.5)
        #   - Append to self.parts

        pass

    def move(self, x, y, z):
        """Move the entire tree (all parts) to a new position.

        Args:
            x (float): X position.
            y (float): Y position.
            z (float): Z position.
        """
        # TODO: Move all parts of the tree to the new position

        pass

    def set_season(self, season):
        """Change the canopy appearance based on season.

        Use Maya's wireframe color override to visually indicate the season:
            "spring" -> green (color index 14)
            "summer" -> dark green (color index 7)
            "autumn" -> yellow/orange (color index 17)
            "winter" -> no canopy visible (hide it or scale to 0)

        Args:
            season (str): One of "spring", "summer", "autumn", "winter".
        """
        # TODO: Validate that season is one of the allowed values

        # TODO: Set the canopy color based on season
        #   Hint: cmds.setAttr(canopy_name + ".overrideEnabled", 1)
        #         cmds.setAttr(canopy_name + ".overrideColor", color_index)

        pass

    # TODO: Add at least ONE more method of your choice. Ideas:
    #   - delete(self): Remove all parts from the scene
    #   - randomize(self): Slightly randomize size for natural variation
    #   - add_fruit(self, count): Add small spheres in the canopy
