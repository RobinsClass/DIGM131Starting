"""
Assignment 7: Main Scene Builder
DIGM 131 - Intro to Scripting for Digital Media

OBJECTIVE:
    Use your Building and Tree classes to construct a small scene in Maya.
    This file demonstrates how classes make it easy to create multiple
    similar objects without repeating code.

REQUIREMENTS:
    1. Create at least 3 Building instances with different sizes
    2. Create at least 5 Tree instances with varying parameters
    3. Arrange them into a simple street or neighborhood layout
    4. Use at least one additional method from each class (windows, season, etc.)
    5. Add comments explaining your scene layout decisions

DELIVERABLES:
    - This file, completed
    - scene_classes.py with both classes completed
"""

import maya.cmds as cmds
from scene_classes import Building, Tree


def clear_scene():
    """Remove all objects from the current Maya scene.

    This is a convenience function so you can re-run your script
    without leftover objects from previous runs.
    """
    # TODO: Use cmds.select(all=True) and cmds.delete() to clear the scene
    #   Wrap in a try/except in case the scene is already empty

    pass


def build_scene():
    """Construct the full scene using Building and Tree instances.

    TODO: Create your scene here. Example layout:

        # Create buildings along a street
        house1 = Building("house1", width=3, height=4, depth=3)
        house1.move(-8, 0, 0)
        house1.add_windows(rows=2, columns=2)

        office = Building("office", width=4, height=10, depth=4)
        office.move(0, 0, 0)
        office.add_windows(rows=5, columns=3)

        shop = Building("shop", width=5, height=3, depth=4)
        shop.move(8, 0, 0)

        # Add trees
        for i in range(5):
            tree = Tree("tree{}".format(i), trunk_height=2 + i * 0.5)
            tree.move(-6 + i * 3, 0, 5)
            tree.set_season("summer")
    """
    # TODO: Create at least 3 buildings with different dimensions

    # TODO: Position each building using the move() method

    # TODO: Add windows to at least one building

    # TODO: Create at least 5 trees with varying sizes

    # TODO: Position trees around your scene

    # TODO: Use set_season() on at least some trees

    # TODO: Use your additional custom methods

    pass


def main():
    """Entry point for the scene builder."""
    clear_scene()
    build_scene()
    print("Scene built successfully!")


if __name__ == "__main__":
    main()
