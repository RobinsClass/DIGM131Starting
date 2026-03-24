"""
DIGM 131 - Assignment 5: Multi-Module Toolkit (material_utils.py)
==================================================================

Material utility functions for creating and assigning shaders in Maya.

This module provides helpers that create Lambert or Blinn shaders with
specified colors and assign them to objects.
"""

import maya.cmds as cmds


def create_material(name="custom_mat", color=(0.5, 0.5, 0.5),
                    material_type="lambert"):
    """Create a new shader and its shading group.

    Args:
        name (str): Name for the shader node.
        color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
        material_type (str): Type of shader to create. Supported values
            are "lambert" and "blinn".

    Returns:
        tuple: (shader_name, shading_group_name) -- the names of the
            created shader node and its associated shading group.
    """
    # TODO: Implement.
    #   1. Create a shader node: cmds.shadingNode(material_type, asShader=True, name=name)
    #   2. Create a shading group: cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG")
    #   3. Connect the shader to the shading group:
    #      cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    #   4. Set the color attribute: cmds.setAttr(shader + ".color", *color, type="double3")
    #   5. Return (shader, sg).
    pass


def assign_material(obj_name, shading_group):
    """Assign an existing shading group to a Maya object.

    Args:
        obj_name (str): The name of the Maya transform or shape node.
        shading_group (str): The name of the shading group (e.g.,
            "red_mat_SG") to assign.

    Returns:
        None
    """
    # TODO: Implement.
    #   Use cmds.sets(obj_name, edit=True, forceElement=shading_group)
    pass


def create_and_assign(obj_name, name="auto_mat", color=(0.5, 0.5, 0.5),
                      material_type="lambert"):
    """Convenience function: create a material and immediately assign it.

    Args:
        obj_name (str): The Maya object to receive the material.
        name (str): Name for the new shader.
        color (tuple): (r, g, b) color, values 0.0 to 1.0.
        material_type (str): "lambert" or "blinn".

    Returns:
        str: The name of the created shader node.
    """
    # TODO: Implement by calling create_material() then assign_material().
    pass
