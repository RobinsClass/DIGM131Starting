"""
DIGM 131 - Week 6 Demo: Debugging with Print Statements
=========================================================
Topics covered:
  - The [DEBUG] print pattern with context and variable state
  - A script that "doesn't work right" and how to diagnose it
  - try/except for graceful error handling
  - cmds.objExists() for safe scene queries
  - Input validation and assert statements

Run this in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds


# ===================================================================
# 1. THE [DEBUG] PRINT PATTERN
#    When something goes wrong, add prints that show:
#      - WHERE you are (which function, which step)
#      - WHAT the variables contain right now
#    Prefix with [DEBUG] so you can find and remove them later.
# ===================================================================

def create_building_row(count, spacing):
    """Create a row of buildings.  Debug prints show execution flow."""
    print("[DEBUG] create_building_row called: count={}, spacing={}".format(
        count, spacing
    ))

    buildings = []
    for i in range(count):
        x_pos = i * spacing
        height = 3 + i * 2

        print("[DEBUG]   Loop i={}: x_pos={}, height={}".format(i, x_pos, height))

        bldg = cmds.polyCube(width=2, height=height, depth=2, name="bldg_#")[0]
        cmds.move(x_pos, height / 2.0, 0, bldg)
        buildings.append(bldg)

    print("[DEBUG] create_building_row returning {} buildings: {}".format(
        len(buildings), buildings
    ))
    return buildings


# ===================================================================
# 2. A BUGGY FUNCTION -- before debugging
#    This function is supposed to scale every building by a factor,
#    but it "doesn't work right."  Let's add debug prints to find out why.
# ===================================================================

def scale_buildings_buggy(building_list, factor):
    """Scale buildings -- but something is wrong..."""
    for i in range(len(building_list)):
        name = building_list[i]
        # BUG: using i as the scale factor instead of 'factor'!
        cmds.scale(i, i, i, name)


def scale_buildings_fixed(building_list, factor):
    """Scale buildings -- fixed version with debug prints."""
    print("[DEBUG] scale_buildings_fixed: {} buildings, factor={}".format(
        len(building_list), factor
    ))

    for i, name in enumerate(building_list):
        print("[DEBUG]   Scaling '{}' by factor {}".format(name, factor))
        # FIX: use 'factor' not 'i'
        cmds.scale(factor, factor, factor, name)


# ===================================================================
# 3. TRY / EXCEPT -- catch errors without crashing
# ===================================================================

def safe_delete(obj_name):
    """Delete an object, handling the case where it doesn't exist.

    Without try/except, deleting a non-existent object crashes.
    With it, we get a friendly warning instead.
    """
    try:
        cmds.delete(obj_name)
        print("Deleted '{}'.".format(obj_name))
    except ValueError:
        print("Warning: '{}' does not exist, skipping delete.".format(obj_name))


# ===================================================================
# 4. cmds.objExists() -- check before you act
# ===================================================================

def move_if_exists(obj_name, x, y, z):
    """Move an object only if it actually exists in the scene.

    This is safer than try/except because it avoids the error entirely.
    """
    if cmds.objExists(obj_name):
        cmds.move(x, y, z, obj_name)
        print("Moved '{}' to ({}, {}, {}).".format(obj_name, x, y, z))
    else:
        print("[WARNING] '{}' not found in scene -- cannot move.".format(obj_name))


# ===================================================================
# 5. INPUT VALIDATION -- catch bad data early
# ===================================================================

def create_safe_building(width=2, height=5, depth=2):
    """Create a building with input validation.

    Catches nonsensical values BEFORE they cause confusing errors
    deep inside Maya.
    """
    # Validate types
    if not isinstance(height, (int, float)):
        print("[ERROR] height must be a number, got: {} ({})".format(
            height, type(height).__name__
        ))
        return None

    # Validate ranges
    if height <= 0:
        print("[ERROR] height must be positive, got: {}".format(height))
        return None

    if width <= 0 or depth <= 0:
        print("[ERROR] width and depth must be positive.")
        return None

    bldg = cmds.polyCube(width=width, height=height, depth=depth, name="bldg_#")[0]
    cmds.move(0, height / 2.0, 0, bldg)
    return bldg


# ===================================================================
# 6. ASSERT -- quick sanity checks during development
#    Asserts are like guardrails.  They crash LOUDLY so you notice
#    bad assumptions immediately.  Remove them before shipping.
# ===================================================================

def set_building_color(building_name, r, g, b):
    """Set building color with assert-based sanity checks."""
    # These asserts catch programmer mistakes early
    assert isinstance(building_name, str), "building_name must be a string"
    assert 0.0 <= r <= 1.0, "Red channel out of range: {}".format(r)
    assert 0.0 <= g <= 1.0, "Green channel out of range: {}".format(g)
    assert 0.0 <= b <= 1.0, "Blue channel out of range: {}".format(b)

    shader = cmds.shadingNode("lambert", asShader=True, name="temp_mat_#")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                   name="temp_SG_#")
    cmds.connectAttr("{}.outColor".format(shader),
                     "{}.surfaceShader".format(sg), force=True)
    cmds.setAttr("{}.color".format(shader), r, g, b, type="double3")
    cmds.sets(building_name, edit=True, forceElement=sg)


# ===================================================================
# 7. RUN THE DEMO
# ===================================================================

def run_demo():
    """Demonstrate all debugging techniques."""
    cmds.file(new=True, force=True)
    print("=" * 50)
    print("  Demo: Debugging with Print Statements")
    print("=" * 50)

    # Create buildings with debug output
    buildings = create_building_row(count=4, spacing=5)

    # Show the buggy version (buildings vanish because scale=0 on first)
    print("\n--- Buggy scale (notice i=0 makes first building disappear) ---")
    scale_buildings_buggy(buildings, factor=1.5)

    # Undo and try the fixed version
    cmds.undo()
    print("\n--- Fixed scale ---")
    scale_buildings_fixed(buildings, factor=1.2)

    # Safe delete
    print("\n--- Safe delete ---")
    safe_delete("does_not_exist")
    safe_delete(buildings[0])

    # objExists check
    print("\n--- objExists check ---")
    move_if_exists("bldg_99", 0, 10, 0)
    move_if_exists(buildings[1], 0, 10, 0)

    # Input validation
    print("\n--- Input validation ---")
    create_safe_building(height=-3)
    create_safe_building(height="tall")
    good_bldg = create_safe_building(height=6)
    print("Valid building:", good_bldg)

    cmds.viewFit(all=True)
    print("\nDemo complete!")


run_demo()
