"""
DIGM 131 - Week 4 Demo: Data-Driven Scripting
===============================================
Topics covered:
  - The list-of-dictionaries pattern
  - Separating DATA from LOGIC
  - Iterating over structured data to generate geometry
  - PEP 8 style (snake_case, spacing, docstrings)

Key idea: instead of writing ten function calls by hand, describe
your scene as DATA and let a loop do the work.

Run this in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds


# ---------------------------------------------------------------------------
# 1. DATA: describe what we want to build
#    Each dictionary is one object.  The keys match the parameters
#    our creation functions expect.
# ---------------------------------------------------------------------------

BUILDINGS = [
    {"width": 2, "height": 6,  "depth": 2, "x": 0,  "z": 0,  "name": "office"},
    {"width": 3, "height": 10, "depth": 3, "x": 5,  "z": 0,  "name": "tower"},
    {"width": 4, "height": 4,  "depth": 3, "x": 10, "z": 0,  "name": "warehouse"},
    {"width": 2, "height": 8,  "depth": 2, "x": 15, "z": 0,  "name": "apartment"},
    {"width": 3, "height": 5,  "depth": 2, "x": 0,  "z": -7, "name": "shop"},
    {"width": 2, "height": 12, "depth": 2, "x": 5,  "z": -7, "name": "skyscraper"},
]

TREES = [
    {"trunk_h": 1.5, "canopy_r": 1.0, "x": 3,  "z": 3},
    {"trunk_h": 1.0, "canopy_r": 0.7, "x": 8,  "z": 3},
    {"trunk_h": 2.0, "canopy_r": 1.2, "x": 13, "z": 3},
    {"trunk_h": 1.2, "canopy_r": 0.9, "x": 3,  "z": -4},
    {"trunk_h": 1.8, "canopy_r": 1.1, "x": 8,  "z": -4},
]


# ---------------------------------------------------------------------------
# 2. LOGIC: functions that know HOW to build, but not WHAT to build
# ---------------------------------------------------------------------------

def create_building(width, height, depth, x, z, name="building"):
    """Create a single building cube placed on the ground plane.

    Args:
        width:  X-axis size.
        height: Y-axis size.
        depth:  Z-axis size.
        x:      World X position.
        z:      World Z position.
        name:   Base name for the Maya node.

    Returns:
        The transform node name.
    """
    cube = cmds.polyCube(
        width=width, height=height, depth=depth,
        name="{}_#".format(name)
    )[0]
    cmds.move(x, height / 2.0, z, cube)
    return cube


def create_tree(trunk_h, canopy_r, x, z):
    """Create a tree from a cylinder trunk and sphere canopy.

    Args:
        trunk_h:  Trunk height.
        canopy_r: Canopy sphere radius.
        x:        World X position.
        z:        World Z position.

    Returns:
        The group node name.
    """
    trunk = cmds.polyCylinder(
        radius=0.15, height=trunk_h, name="trunk_#"
    )[0]
    cmds.move(x, trunk_h / 2.0, z, trunk)

    canopy = cmds.polySphere(radius=canopy_r, name="canopy_#")[0]
    cmds.move(x, trunk_h + canopy_r * 0.7, z, canopy)

    return cmds.group(trunk, canopy, name="tree_#")


def create_ground(size=30):
    """Create a flat ground plane centered at the origin."""
    ground = cmds.polyPlane(
        width=size, height=size,
        subdivisionsX=1, subdivisionsY=1,
        name="ground"
    )[0]
    return ground


# ---------------------------------------------------------------------------
# 3. DRIVER: iterate over data and call the functions
# ---------------------------------------------------------------------------

def build_scene():
    """Read the data lists and generate the full scene."""
    cmds.file(new=True, force=True)
    print("--- Demo: Data-Driven Scene Generation ---")

    # Ground
    create_ground()

    # Buildings -- unpack each dict with **
    for info in BUILDINGS:
        bldg = create_building(**info)
        print("Created building: {}".format(bldg))

    # Trees
    for info in TREES:
        tree = create_tree(**info)
        print("Created tree: {}".format(tree))

    cmds.viewFit(all=True)
    print("Scene complete! {} buildings, {} trees.".format(
        len(BUILDINGS), len(TREES)
    ))


# ---------------------------------------------------------------------------
# 4. RUN
# ---------------------------------------------------------------------------
build_scene()
