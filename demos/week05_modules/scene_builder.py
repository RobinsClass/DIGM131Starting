"""
scene_builder.py -- Main script that builds a complete city scene.
==================================================================
DIGM 131 - Week 5

This script imports from geometry_utils and material_utils to
assemble a scene.  It demonstrates:
  - Importing your own modules
  - Using aliased imports for readability
  - The if __name__ == "__main__": pattern
  - Keeping the main script focused on high-level logic

Run this file directly in Maya (or source it from the Script Editor).
"""

import os
import sys

import maya.cmds as cmds

# --- Ensure sibling modules are importable ---
# Add this file's directory to Python's search path so that
# "import geometry_utils" works even if Maya doesn't know the folder.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

# Now import our custom modules with short aliases
import geometry_utils as geo
import material_utils as mat


# -------------------------------------------------------------------
# Scene data -- positions and settings for our city
# -------------------------------------------------------------------
BUILDING_DATA = [
    {"width": 3, "height": 8,  "depth": 3, "position": (-6, 0, 0)},
    {"width": 2, "height": 12, "depth": 2, "position": (-2, 0, 0)},
    {"width": 4, "height": 5,  "depth": 3, "position": (3, 0, 0)},
    {"width": 2, "height": 9,  "depth": 2, "position": (8, 0, 0)},
    {"width": 3, "height": 6,  "depth": 3, "position": (12, 0, 0)},
]

TREE_POSITIONS = [
    (-9, 0, 4), (-4, 0, 5), (1, 0, 4), (6, 0, 5), (11, 0, 4),
]

LAMP_POSITIONS = [
    (-8, 0, -3), (0, 0, -3), (7, 0, -3), (14, 0, -3),
]

BUILDING_COLORS = [
    ("brick_red",    (0.72, 0.22, 0.15)),
    ("concrete",     (0.65, 0.65, 0.62)),
    ("steel_blue",   (0.35, 0.50, 0.68)),
    ("sandstone",    (0.82, 0.72, 0.55)),
    ("slate_gray",   (0.45, 0.48, 0.52)),
]


def build_city_scene():
    """Assemble a small city scene using geometry and material utils."""
    cmds.file(new=True, force=True)
    print("=== Building City Scene ===")

    # Ground plane
    ground = geo.create_ground(size=40)
    ground_mat = mat.create_material("ground_gray", (0.35, 0.38, 0.32))
    mat.assign_material(ground, ground_mat)

    # Buildings with matching colors
    for i, data in enumerate(BUILDING_DATA):
        bldg = geo.create_building(**data)
        color_name, color_rgb = BUILDING_COLORS[i % len(BUILDING_COLORS)]
        shader = mat.create_material(color_name, color_rgb)
        mat.assign_material(bldg, shader)
        print("  Built: {} with {}".format(bldg, color_name))

    # Trees with a shared green material
    tree_green = mat.create_material("tree_green", (0.18, 0.55, 0.15))
    for pos in TREE_POSITIONS:
        tree = geo.create_tree(position=pos)
        mat.assign_material(tree, tree_green)

    # Lamp posts
    for pos in LAMP_POSITIONS:
        geo.create_lamp_post(position=pos)

    # Final touches
    cmds.viewFit(all=True)
    print("=== Scene Complete ===")
    print("  {} buildings, {} trees, {} lamps".format(
        len(BUILDING_DATA), len(TREE_POSITIONS), len(LAMP_POSITIONS)
    ))


# -------------------------------------------------------------------
# Entry point -- only runs when this file is executed directly.
# If another script does "import scene_builder", this block is
# skipped, so they can call build_city_scene() themselves.
# -------------------------------------------------------------------
if __name__ == "__main__":
    build_city_scene()
