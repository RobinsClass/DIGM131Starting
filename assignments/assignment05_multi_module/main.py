"""
DIGM 131 - Assignment 5: Multi-Module Toolkit (main.py)
========================================================

Main entry point that imports and uses all utility modules to build a scene.

PROJECT STRUCTURE:
    assignment05_multi_module/
        geometry_utils.py   -- Functions for creating 3D primitives.
        material_utils.py   -- Functions for creating and assigning shaders.
        layout_utils.py     -- Functions for arranging objects spatially.
        main.py             -- This file; orchestrates the scene build.
        README.txt          -- Describes the project and how to run it.

REQUIREMENTS:
    1. Import and use functions from ALL three utility modules.
    2. Create at least 15 objects using geometry_utils.
    3. Apply materials to at least 5 objects using material_utils.
    4. Use at least 2 different layout functions from layout_utils.
    5. The final scene should be visually cohesive and well-organized.

GRADING CRITERIA:
    - [20%] All three modules are imported and used correctly.
    - [20%] 15+ objects created via geometry_utils functions.
    - [20%] Materials applied to 5+ objects via material_utils.
    - [15%] 2+ layout functions used from layout_utils.
    - [15%] Scene is visually coherent and intentional.
    - [10%] Code is clean, well-commented, and follows PEP 8.
"""

import maya.cmds as cmds

# Import your utility modules.
import geometry_utils as geo
import material_utils as mat
import layout_utils as lay


def build_scene():
    """Build the complete scene using all utility modules.

    This function should:
        1. Create geometry with geo.create_box(), geo.create_cylinder(), etc.
        2. Create and assign materials with mat.create_and_assign() or
           mat.create_material() + mat.assign_material().
        3. Arrange some objects with lay.arrange_in_line(),
           lay.arrange_in_grid(), or lay.arrange_in_circle().
    """
    # --- Ground plane ---
    ground = cmds.polyPlane(name="ground", width=60, height=60,
                            subdivisionsX=1, subdivisionsY=1)[0]

    # TODO: Create objects using geometry_utils.
    # Example:
    #   tower = geo.create_box(name="tower", width=3, height=12, depth=3,
    #                          position=(-10, 0, 0))

    # TODO: Create and assign materials using material_utils.
    # Example:
    #   mat.create_and_assign(tower, name="tower_mat",
    #                         color=(0.4, 0.4, 0.6))

    # TODO: Arrange some objects using layout_utils.
    # Example:
    #   posts = [geo.create_cylinder(name="post_{}".format(i), radius=0.2,
    #            height=3) for i in range(8)]
    #   lay.arrange_in_circle(posts, radius=12)

    pass  # Remove once you add your code.


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.file(new=True, force=True)
    build_scene()
    cmds.viewFit(allObjects=True)
    print("Multi-module scene built successfully!")
