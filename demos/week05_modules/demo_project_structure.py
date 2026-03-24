"""
DIGM 131 - Week 5 Demo: Project Structure & Modules
=====================================================
This is a SINGLE FILE that EXPLAINS how a multi-file Maya project
is organized.  Read through the comments, then look at the actual
module files (geometry_utils.py, material_utils.py, scene_builder.py)
that accompany this demo.

Topics covered:
  - Why we split code into modules
  - import patterns (import, from ... import, as)
  - The if __name__ == "__main__": guard
  - How Maya finds your scripts (sys.path)
"""

# ===================================================================
# WHY MODULES?
# ===================================================================
# When a script grows past ~100 lines, it becomes hard to navigate.
# Modules let us:
#   1. Group related functions into their own files
#   2. Reuse code across projects (import once, use everywhere)
#   3. Test pieces independently
# A typical Maya tool project might look like this:
#   my_city_tool/
#       geometry_utils.py    <-- functions that create geometry
#       material_utils.py    <-- functions that create materials
#       scene_builder.py     <-- main script that ties it together
# Each .py file is a MODULE.  The folder is a PACKAGE (if it
# contains an __init__.py, but we'll keep it simple for now).


# ===================================================================
# IMPORT PATTERNS
# ===================================================================
import maya.cmds as cmds  # We've been doing this all along!

# Pattern 1: import the whole module, use dot notation
# ----------------------------------------------------
#   import geometry_utils
#   geometry_utils.create_building(height=10)
# Pro: crystal clear where every function comes from.
# Con: more typing.

# Pattern 2: import specific functions
# ----------------------------------------------------
#   from geometry_utils import create_building, create_tree
#   create_building(height=10)
# Pro: shorter calls.
# Con: less obvious which module a function belongs to.

# Pattern 3: import with alias
# ----------------------------------------------------
#   import geometry_utils as geo
#   geo.create_building(height=10)
# Pro: short AND clear.  This is often the best choice.

# Pattern 4 (AVOID): wildcard import
# ----------------------------------------------------
#   from geometry_utils import *
#   create_building(height=10)
# Con: you can't tell where anything comes from.
#      Names may collide silently.  Don't do this.


# ===================================================================
# MAKING MAYA FIND YOUR MODULES
# ===================================================================
# Maya only imports from folders on its search path.
# You can add your project folder like this:

import sys
import os

# Get the directory THIS file lives in
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Add it to sys.path so Python can find sibling modules
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

# Now imports from the same folder will work:
#   import geometry_utils


# ===================================================================
# THE  if __name__ == "__main__":  GUARD
# ===================================================================
# Every Python file has a hidden variable called __name__.
#   - When you RUN the file directly, __name__ is "__main__".
#   - When another file IMPORTS it, __name__ is the module name
#     (e.g., "geometry_utils").
# This lets you put demo/test code that only runs when the file
# is executed directly, not when it's imported:
#   def create_building(height=5):
#       ...
#   if __name__ == "__main__":
#       # This only runs if you execute geometry_utils.py directly
#       create_building(height=10)
#       print("Test building created!")


# ===================================================================
# EXAMPLE: what each file in our project contains
# ===================================================================

# --- geometry_utils.py would contain: ---
#   import maya.cmds as cmds
#   def create_building(width=2, height=5, depth=2, position=(0,0,0)):
#       """Create a building cube on the ground plane."""
#       ...
#       return building_name
#   def create_tree(trunk_height=1.5, canopy_radius=1.0, position=(0,0,0)):
#       """Create a tree from cylinder + sphere."""
#       ...
#       return tree_group
#   if __name__ == "__main__":
#       cmds.file(new=True, force=True)
#       create_building()
#       create_tree(position=(5, 0, 0))
#       print("geometry_utils self-test passed!")


# --- material_utils.py would contain: ---
#   import maya.cmds as cmds
#   import random
#   def create_material(name, color):
#       """Create a Lambert shader with the given RGB color."""
#       ...
#       return shader_name
#   def assign_material(obj_name, shader_name):
#       """Assign an existing shader to an object."""
#       ...
#   if __name__ == "__main__":
#       cmds.file(new=True, force=True)
#       cube = cmds.polyCube()[0]
#       mat = create_material("test_red", (1, 0, 0))
#       assign_material(cube, mat)
#       print("material_utils self-test passed!")


# --- scene_builder.py (the main script) would contain: ---
#   import geometry_utils as geo
#   import material_utils as mat
#   def build_scene():
#       geo.create_ground()
#       bldg = geo.create_building(height=8)
#       red = mat.create_material("red_mat", (0.8, 0.2, 0.1))
#       mat.assign_material(bldg, red)
#   if __name__ == "__main__":
#       build_scene()


# ===================================================================
# LIVE DEMO: use the actual modules next to this file
# ===================================================================

def run_demo():
    """Import and use the real companion modules."""
    # These imports work because we added THIS_DIR to sys.path above
    import geometry_utils as geo
    import material_utils as mat

    cmds.file(new=True, force=True)
    print("--- Demo: Project Structure & Imports ---")

    geo.create_ground(size=20)

    bldg = geo.create_building(width=3, height=8, depth=3)
    red = mat.create_material("demo_red", (0.8, 0.15, 0.1))
    mat.assign_material(bldg, red)

    tree = geo.create_tree(position=(6, 0, 0))
    green = mat.create_material("demo_green", (0.2, 0.7, 0.15))
    mat.assign_material(tree, green)

    lamp = geo.create_lamp_post(position=(-4, 0, 0))

    cmds.viewFit(all=True)
    print("Demo complete!  Modules successfully imported and used.")


if __name__ == "__main__":
    run_demo()
