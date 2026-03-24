"""
geometry_utils.py -- Reusable geometry creation functions for Maya.
==================================================================
DIGM 131 - Week 5

This module provides simple functions for creating common scene
objects: buildings, trees, lamp posts, and a ground plane.

Usage:
    import geometry_utils as geo
    geo.create_building(width=3, height=8, depth=3)
"""

import maya.cmds as cmds


def create_building(width=2, height=5, depth=2, position=(0, 0, 0)):
    """Create a building as a poly cube sitting on the ground plane.

    Args:
        width (float):    X-axis dimension.  Default 2.
        height (float):   Y-axis dimension.  Default 5.
        depth (float):    Z-axis dimension.  Default 2.
        position (tuple): (x, y, z) world position of the base center.

    Returns:
        str: Name of the created transform node.
    """
    building = cmds.polyCube(
        width=width,
        height=height,
        depth=depth,
        name="building_#"
    )[0]

    # Shift up so the base sits at y = position[1]
    cmds.move(
        position[0],
        position[1] + height / 2.0,
        position[2],
        building
    )
    return building


def create_tree(trunk_height=1.5, canopy_radius=1.0, position=(0, 0, 0)):
    """Create a tree from a cylinder trunk and sphere canopy.

    Args:
        trunk_height (float):  Height of the trunk.     Default 1.5.
        canopy_radius (float): Radius of the canopy.    Default 1.0.
        position (tuple):      (x, y, z) base position.

    Returns:
        str: Name of the group containing trunk and canopy.
    """
    trunk = cmds.polyCylinder(
        radius=0.15,
        height=trunk_height,
        name="trunk_#"
    )[0]
    cmds.move(position[0], position[1] + trunk_height / 2.0, position[2], trunk)

    canopy = cmds.polySphere(radius=canopy_radius, name="canopy_#")[0]
    canopy_y = position[1] + trunk_height + canopy_radius * 0.7
    cmds.move(position[0], canopy_y, position[2], canopy)

    tree_group = cmds.group(trunk, canopy, name="tree_#")
    return tree_group


def create_lamp_post(height=4, position=(0, 0, 0)):
    """Create a lamp post from a thin cylinder and a small sphere on top.

    Args:
        height (float):   Total height of the post.  Default 4.
        position (tuple): (x, y, z) base position.

    Returns:
        str: Name of the group containing pole and lamp.
    """
    # Pole
    pole = cmds.polyCylinder(
        radius=0.08,
        height=height,
        name="lamp_pole_#"
    )[0]
    cmds.move(position[0], position[1] + height / 2.0, position[2], pole)

    # Lamp head -- small glowing sphere at the top
    lamp_head = cmds.polySphere(radius=0.3, name="lamp_head_#")[0]
    cmds.move(position[0], position[1] + height + 0.15, position[2], lamp_head)

    lamp_group = cmds.group(pole, lamp_head, name="lamp_post_#")
    return lamp_group


def create_ground(size=30):
    """Create a flat ground plane centered at the origin.

    Args:
        size (float): Width and depth of the plane.  Default 30.

    Returns:
        str: Name of the ground plane transform node.
    """
    ground = cmds.polyPlane(
        width=size,
        height=size,
        subdivisionsX=1,
        subdivisionsY=1,
        name="ground"
    )[0]
    return ground


# -------------------------------------------------------------------
# Self-test: runs only when this file is executed directly,
# NOT when it is imported by another script.
# -------------------------------------------------------------------
if __name__ == "__main__":
    cmds.file(new=True, force=True)

    create_ground()
    create_building(height=7, position=(0, 0, 0))
    create_tree(position=(5, 0, 0))
    create_lamp_post(position=(-3, 0, 0))

    cmds.viewFit(all=True)
    print("geometry_utils self-test complete -- check viewport.")
