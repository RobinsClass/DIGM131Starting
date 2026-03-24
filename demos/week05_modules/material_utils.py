"""
material_utils.py -- Material and shading helper functions for Maya.
====================================================================
DIGM 131 - Week 5

This module provides convenience functions for creating Lambert
materials, assigning them to objects, and generating random colors.

Usage:
    import material_utils as mat
    red = mat.create_material("brick_red", (0.7, 0.15, 0.1))
    mat.assign_material("building_1", red)
"""

import maya.cmds as cmds
import random


def create_material(name, color=(0.5, 0.5, 0.5)):
    """Create a Lambert shader with the given name and RGB color.

    If a shader with this name already exists, it is returned
    without creating a duplicate.

    Args:
        name (str):   Name for the shader node.
        color (tuple): (R, G, B) floats, each 0.0 - 1.0.  Default mid-gray.

    Returns:
        str: The name of the shader node.
    """
    # Avoid duplicates
    if cmds.objExists(name):
        return name

    # Create shader and shading group
    shader = cmds.shadingNode("lambert", asShader=True, name=name)
    shading_group = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name="{}_SG".format(name)
    )

    # Connect shader -> shading group
    cmds.connectAttr(
        "{}.outColor".format(shader),
        "{}.surfaceShader".format(shading_group),
        force=True
    )

    # Set the color
    cmds.setAttr("{}.color".format(shader), *color, type="double3")

    return shader


def assign_material(obj_name, shader_name):
    """Assign an existing shader to a Maya object.

    Args:
        obj_name (str):    Name of the transform or shape node.
        shader_name (str): Name of the shader (e.g., a Lambert node).

    Raises:
        RuntimeError: If the object or shader does not exist.
    """
    if not cmds.objExists(obj_name):
        cmds.warning("assign_material: '{}' does not exist.".format(obj_name))
        return

    if not cmds.objExists(shader_name):
        cmds.warning("assign_material: shader '{}' not found.".format(shader_name))
        return

    # Find the shading group connected to this shader
    shading_groups = cmds.listConnections(
        "{}.outColor".format(shader_name), type="shadingEngine"
    )

    if not shading_groups:
        cmds.warning("No shading group found for '{}'.".format(shader_name))
        return

    # Add the object to the shading group's member set
    cmds.sets(obj_name, edit=True, forceElement=shading_groups[0])


def create_random_color_material(base_name="random_mat"):
    """Create a Lambert shader with a random RGB color.

    Useful for quick prototyping and visual variety.

    Args:
        base_name (str): Prefix for the shader name.  A random suffix
                         is appended to avoid name collisions.

    Returns:
        str: The name of the newly created shader.
    """
    # Generate a random color
    r = random.uniform(0.1, 1.0)
    g = random.uniform(0.1, 1.0)
    b = random.uniform(0.1, 1.0)

    # Build a unique name using the color values
    unique_name = "{}_{:02x}{:02x}{:02x}".format(
        base_name, int(r * 255), int(g * 255), int(b * 255)
    )

    return create_material(unique_name, (r, g, b))


# -------------------------------------------------------------------
# Self-test
# -------------------------------------------------------------------
if __name__ == "__main__":
    cmds.file(new=True, force=True)

    # Create a cube and assign a red material
    test_cube = cmds.polyCube(name="test_cube")[0]
    red = create_material("test_red", (0.9, 0.1, 0.1))
    assign_material(test_cube, red)

    # Create a sphere with a random color
    test_sphere = cmds.polySphere(name="test_sphere")[0]
    cmds.move(3, 0, 0, test_sphere)
    rand_mat = create_random_color_material()
    assign_material(test_sphere, rand_mat)

    cmds.viewFit(all=True)
    print("material_utils self-test complete -- check viewport.")
