"""
DIGM 131 - Week 4 Demo: Default Parameters & Function Composition
=================================================================
Topics covered:
  - Default parameter values
  - Keyword arguments (calling by name)
  - Functions calling other functions (composition)
  - Building a vocabulary of small, reusable functions

Run this in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds


# ---------------------------------------------------------------------------
# 1. DEFAULT PARAMETERS
#    If the caller doesn't pass a value, the default kicks in.
#    This lets one function handle many variations.
# ---------------------------------------------------------------------------

def create_building(width=2, height=5, depth=2, position=(0, 0, 0)):
    """Create a simple building (cube) with sensible defaults.

    Args:
        width:    How wide the building is (X axis). Default 2.
        height:   How tall the building is (Y axis). Default 5.
        depth:    How deep the building is (Z axis). Default 2.
        position: (x, y, z) tuple for placement.  Default origin.

    Returns:
        The name of the created cube transform node.
    """
    # Create the cube with the given dimensions
    building = cmds.polyCube(
        width=width,
        height=height,
        depth=depth,
        name="building_#"
    )[0]

    # Lift it so the base sits on the ground plane (y=0)
    cmds.move(
        position[0],
        position[1] + height / 2.0,
        position[2],
        building
    )

    return building


def create_tree(trunk_height=1.5, canopy_radius=1.0, position=(0, 0, 0)):
    """Create a simple tree from a cylinder (trunk) and sphere (canopy).

    Args:
        trunk_height:   Height of the trunk cylinder.  Default 1.5.
        canopy_radius:  Radius of the leafy sphere.    Default 1.0.
        position:       (x, y, z) world position.      Default origin.

    Returns:
        The name of the group containing trunk and canopy.
    """
    # --- Trunk ---
    trunk = cmds.polyCylinder(
        radius=0.15,
        height=trunk_height,
        name="trunk_#"
    )[0]
    cmds.move(
        position[0],
        position[1] + trunk_height / 2.0,
        position[2],
        trunk
    )

    # --- Canopy ---
    canopy = cmds.polySphere(
        radius=canopy_radius,
        name="canopy_#"
    )[0]
    cmds.move(
        position[0],
        position[1] + trunk_height + canopy_radius * 0.7,
        position[2],
        canopy
    )

    # Group them so the tree moves as one object
    tree_group = cmds.group(trunk, canopy, name="tree_#")
    return tree_group


# ---------------------------------------------------------------------------
# 2. KEYWORD ARGUMENTS
#    You can pass arguments by name in any order.
#    This makes function calls self-documenting.
# ---------------------------------------------------------------------------

# These two calls produce the SAME result:
#   create_building(3, 8, 3, (0, 0, 0))          # positional
#   create_building(height=8, width=3, depth=3)   # keyword (clearer!)


# ---------------------------------------------------------------------------
# 3. FUNCTION COMPOSITION: create_city_block()
#    A higher-level function that calls our smaller building blocks.
#    This is the payoff: small functions become a creative vocabulary.
# ---------------------------------------------------------------------------

def create_city_block(num_buildings=4, spacing=5, add_trees=True):
    """Compose a row of buildings with optional trees between them.

    This function doesn't create geometry directly -- it delegates
    to create_building() and create_tree().  That separation keeps
    each function short and easy to understand.

    Args:
        num_buildings: How many buildings in the row.  Default 4.
        spacing:       Distance between building centers. Default 5.
        add_trees:     Place a tree between each building? Default True.

    Returns:
        The name of a group containing the whole city block.
    """
    all_objects = []

    for i in range(num_buildings):
        x_pos = i * spacing

        # Vary the building height so the skyline looks interesting
        height = 4 + (i % 3) * 3  # cycles through 4, 7, 10, 4, ...

        # Call our building function with keyword arguments
        bldg = create_building(
            width=2,
            height=height,
            depth=2,
            position=(x_pos, 0, 0)
        )
        all_objects.append(bldg)

        # Place a tree between buildings (not after the last one)
        if add_trees and i < num_buildings - 1:
            tree_x = x_pos + spacing / 2.0
            tree = create_tree(
                trunk_height=1.0,
                canopy_radius=0.8,
                position=(tree_x, 0, 0)
            )
            all_objects.append(tree)

    # Group everything into one tidy node
    block_group = cmds.group(all_objects, name="city_block_#")
    return block_group


# ---------------------------------------------------------------------------
# 4. RUN THE DEMO
# ---------------------------------------------------------------------------

def run_demo():
    """Entry point -- clears the scene and builds a city block."""
    # Start fresh so repeated runs don't pile up
    cmds.file(new=True, force=True)

    print("--- Demo: Default Parameters & Function Composition ---")

    # A single building using ALL defaults
    b1 = create_building()
    print("Default building:", b1)

    # A tall, narrow tower using keyword arguments
    b2 = create_building(width=1, height=12, depth=1, position=(5, 0, 0))
    print("Tall tower:", b2)

    # A standalone tree
    t1 = create_tree(position=(10, 0, 0))
    print("Tree:", t1)

    # A full city block -- composition in action
    block = create_city_block(num_buildings=5, spacing=6, add_trees=True)
    print("City block:", block)

    # Frame everything in the viewport
    cmds.viewFit(all=True)
    print("Done!  Check your viewport.")


# This lets us run the demo by sourcing the file
run_demo()
