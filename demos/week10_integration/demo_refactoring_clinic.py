"""
DIGM 131 - Week 10 Demo: Refactoring Clinic
=============================================
This file shows a BEFORE and AFTER of the same tool.

The BEFORE code works, but it's messy: hard to read, fragile,
repetitive, and impossible to maintain.  The AFTER code does
the exact same thing but is clean, documented, and robust.

Study the differences -- these are the habits that separate
hobbyist scripts from professional tools.
"""

import maya.cmds as cmds
import random

# ************************************************************
#  BEFORE  --  "It works, ship it"
# ************************************************************
# Problems are marked with ### comments.

def do_stuff():  ### Vague name -- what stuff?
    ### No docstring.
    ### One giant function doing everything.

    # hardcoded values everywhere
    for i in range(10):  ### Magic number 10
        t = cmds.polyCube(n="thing_" + str(i))  ### "thing" -- what is it?
        x = random.uniform(-10, 10)  ### Magic numbers -10, 10
        z = random.uniform(-10, 10)
        cmds.move(x, 0, z, t[0])

        ### Duplicated color logic -- copy-pasted for each color case
        if i % 3 == 0:
            s = cmds.shadingNode("lambert", asShader=True)
            cmds.setAttr(s + ".color", 1, 0, 0, type="double3")
            cmds.select(t[0])
            cmds.hyperShade(assign=s)
        elif i % 3 == 1:
            s = cmds.shadingNode("lambert", asShader=True)
            cmds.setAttr(s + ".color", 0, 1, 0, type="double3")
            cmds.select(t[0])
            cmds.hyperShade(assign=s)
        else:
            s = cmds.shadingNode("lambert", asShader=True)
            cmds.setAttr(s + ".color", 0, 0, 1, type="double3")
            cmds.select(t[0])
            cmds.hyperShade(assign=s)

        ### No error handling -- if polyCube fails, everything explodes.
        ### The user must Ctrl+Z ten times to undo because there's no
        ### undo chunk.

    ### Scale some of them, but the logic is tangled in here too
    all = cmds.ls("thing_*")  ### 'all' shadows the built-in all()
    for a in all:
        sv = random.uniform(0.5, 2.0)
        cmds.scale(sv, sv, sv, a)

    print("done")  ### Unhelpful message

# do_stuff()  # Uncomment to run the messy version


# ************************************************************
#  AFTER  --  Refactored version
# ************************************************************
# Same functionality, but:
#   - Clear function names and docstrings
#   - Extracted reusable helper functions
#   - No duplicated code
#   - Named constants instead of magic numbers
#   - Error handling
#   - Undo chunking
#   - Clean separation of concerns

# --- Constants ---
DEFAULT_COUNT = 10
SCATTER_RADIUS = 10.0
SCALE_MIN = 0.5
SCALE_MAX = 2.0

COLOR_PALETTE = [
    (1.0, 0.0, 0.0),   # red
    (0.0, 1.0, 0.0),   # green
    (0.0, 0.0, 1.0),   # blue
]


def apply_color(obj, rgb):
    """Apply an RGB color to a Maya object via a new lambert shader.

    Args:
        obj (str): Name of the Maya transform node.
        rgb (tuple): (r, g, b) floats in 0-1 range.
    """
    if not cmds.objExists(obj):
        cmds.warning(f"apply_color: '{obj}' does not exist.")
        return
    shader = cmds.shadingNode("lambert", asShader=True)
    cmds.setAttr(shader + ".color", rgb[0], rgb[1], rgb[2], type="double3")
    cmds.select(obj)
    cmds.hyperShade(assign=shader)


def create_scattered_cube(name, radius):
    """Create a polyCube at a random XZ position within the given radius.

    Args:
        name (str): Name for the new cube.
        radius (float): Maximum distance from the origin on X and Z.

    Returns:
        str: The Maya node name, or None on failure.
    """
    try:
        node = cmds.polyCube(name=name)[0]
    except RuntimeError as e:
        cmds.warning(f"Failed to create cube '{name}': {e}")
        return None

    x = random.uniform(-radius, radius)
    z = random.uniform(-radius, radius)
    cmds.move(x, 0, z, node)
    return node


def randomize_scale(obj, min_scale, max_scale):
    """Apply a random uniform scale to an object.

    Args:
        obj (str): Maya transform node name.
        min_scale (float): Minimum scale factor.
        max_scale (float): Maximum scale factor.
    """
    if not cmds.objExists(obj):
        cmds.warning(f"randomize_scale: '{obj}' does not exist.")
        return
    s = random.uniform(min_scale, max_scale)
    cmds.scale(s, s, s, obj)


def scatter_colored_cubes(count=DEFAULT_COUNT, radius=SCATTER_RADIUS):
    """Create scattered cubes with cycling colors and random scales.

    This is the main entry point for the tool.  The entire operation
    is wrapped in an undo chunk so the user can undo it all at once.

    Args:
        count (int): Number of cubes to create.
        radius (float): Scatter radius around the origin.
    """
    created_nodes = []

    cmds.undoInfo(openChunk=True)
    try:
        for i in range(count):
            node = create_scattered_cube(f"scatter_cube_{i}", radius)
            if node is None:
                continue  # skip failures gracefully

            # Cycle through the color palette
            color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
            apply_color(node, color)

            randomize_scale(node, SCALE_MIN, SCALE_MAX)
            created_nodes.append(node)

    finally:
        # Always close the undo chunk, even if an error occurred.
        cmds.undoInfo(closeChunk=True)

    print(f"Created {len(created_nodes)} scattered cubes (radius={radius}).")
    return created_nodes


# --- Run the refactored version ---
# scatter_colored_cubes()


# ************************************************************
#  SIDE-BY-SIDE SUMMARY
# ************************************************************
"""
BEFORE                              AFTER
------                              -----
do_stuff()                          scatter_colored_cubes(count, radius)
  - vague name                        - descriptive name
  - no docstring                      - docstring explains args & behavior
  - magic numbers                     - named constants
  - copy-pasted color code x3         - apply_color() helper
  - no error handling                 - try/except, cmds.warning
  - no undo chunk                     - undo chunk wraps everything
  - shadows built-in 'all'            - descriptive variable names
  - "done" print                      - informative summary message
  - one monolithic function           - small focused functions

KEY REFACTORING MOVES:
  1. EXTRACT FUNCTION  -- Pull repeated logic into a helper.
  2. NAME THINGS       -- Variables, functions, constants.
  3. ADD GUARD CLAUSES -- Check for errors early, warn clearly.
  4. USE CONSTANTS     -- Replace magic numbers at the top of the file.
  5. ADD DOCSTRINGS    -- Future-you will thank present-you.
  6. UNDO CHUNK        -- Respect the artist's workflow.
"""
