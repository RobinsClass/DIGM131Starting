"""
DIGM 131 - Week 3 Demo: Introduction to Functions
===================================================
    This demo motivates functions by showing copy-pasted code, then refactoring it
    into reusable functions. Covers def, parameters, default values, return values,
    and variable scope. Builds utility functions students will reuse in later demos.
    Run in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds
import math

cmds.file(new=True, force=True)

# =============================================================================
# SECTION 1: The problem — duplicated code
# =============================================================================
# Watch how painful it is to add a fourth tree."

# Tree 1 — copy-pasted block
trunk1 = cmds.polyCylinder(name="trunk1", radius=0.3, height=2.0)[0]
cmds.move(-4, 1.0, 0, trunk1)
canopy1 = cmds.polySphere(name="canopy1", radius=1.2)[0]
cmds.move(-4, 2.7, 0, canopy1)

# Tree 2 — same thing again
trunk2 = cmds.polyCylinder(name="trunk2", radius=0.3, height=2.0)[0]
cmds.move(0, 1.0, 0, trunk2)
canopy2 = cmds.polySphere(name="canopy2", radius=1.2)[0]
cmds.move(0, 2.7, 0, canopy2)

# Tree 3 — and again...
trunk3 = cmds.polyCylinder(name="trunk3", radius=0.3, height=2.0)[0]
cmds.move(4, 1.0, 0, trunk3)
canopy3 = cmds.polySphere(name="canopy3", radius=1.2)[0]
cmds.move(4, 2.7, 0, canopy3)

# If we want 20 trees, we'd need 20 copies. Functions solve this."

# Clean up before the refactored version
cmds.file(new=True, force=True)

# =============================================================================
# SECTION 2: Defining a function — def, parameters, body
# =============================================================================
# Syntax:  def function_name(parameter1, parameter2):

def create_tree(x, z, trunk_height=2.0, canopy_radius=1.2):
    """Create a simple tree at the given X, Z position.

    Default parameter values (trunk_height=2.0) let callers omit arguments they're happy with.
    """
    trunk_radius = 0.3
    trunk = cmds.polyCylinder(radius=trunk_radius, height=trunk_height)[0]
    cmds.move(x, trunk_height / 2.0, z, trunk)

    canopy = cmds.polySphere(radius=canopy_radius)[0]
    canopy_y = trunk_height + canopy_radius * 0.6
    cmds.move(x, canopy_y, z, canopy)

    # We return the node names so the caller can modify them later if needed.
    return trunk, canopy


create_tree(-4, 0)
create_tree(0, 0)
create_tree(4, 0)

# With custom sizes — override the defaults
create_tree(8, 0, trunk_height=3.5, canopy_radius=1.8)  # a big tree

# =============================================================================
# SECTION 3: Another function — create_building()
# =============================================================================

def create_building(x, z, width=2.0, height=5.0, depth=2.0):
    """Create a rectangular building at (x, z), sitting on the ground plane."""
    building = cmds.polyCube(width=width, height=height, depth=depth)[0]
    cmds.move(x, height / 2.0, z, building)
    return building

# Now we can build a street in just a few lines
create_building(-6, -6, height=8)
create_building(-2, -6, width=3, height=4, depth=3)
create_building(3, -6, height=10)

# =============================================================================
# SECTION 4: Return values — using what a function gives back
# =============================================================================

def create_lamppost(x, z, height=3.0):
    """Create a lamppost and return the pole and lamp node names."""
    pole = cmds.polyCylinder(radius=0.1, height=height)[0]
    cmds.move(x, height / 2.0, z, pole)

    lamp = cmds.polySphere(radius=0.25)[0]
    cmds.move(x, height + 0.25, z, lamp)
    return pole, lamp

# Capture the return values in variables
pole_node, lamp_node = create_lamppost(6, -3)
print("Created lamppost: pole={}, lamp={}".format(pole_node, lamp_node))

# Now we can do something with the returned names — like make the lamp glow
lamp_shader = cmds.shadingNode("lambert", asShader=True, name="lampGlow")
cmds.setAttr(lamp_shader + ".color", 1.0, 0.95, 0.6, type="double3")
cmds.select(lamp_node)
cmds.hyperShade(assign=lamp_shader)

# =============================================================================
# SECTION 5: Variable scope — local vs. outer
# =============================================================================

outer_message = "I'm defined outside"

def demonstrate_scope():
    inner_message = "I'm defined inside"
    print("Inside the function, I can see:", inner_message)
    print("I can also see outer variables:", outer_message)

demonstrate_scope()
# print(inner_message)  # NameError! inner_message doesn't exist out here.

# This is a GOOD thing — it means functions don't accidentally interfere with each other."

# =============================================================================
# SECTION 6: Utility function — place_in_circle()
# =============================================================================
# function that places any creation function's results in a circle."

def place_in_circle(create_func, count, radius, center_x=0, center_z=0):
    """Call create_func repeatedly, placing results in a circle.

    create_func must accept (x, z) as its first two arguments.
    Returns a list of whatever create_func returns.
    """
    results = []
    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = center_x + math.cos(angle) * radius
        z = center_z + math.sin(angle) * radius
        result = create_func(x, z)
        results.append(result)
    return results

# A ring of trees!
place_in_circle(create_tree, count=8, radius=7, center_x=0, center_z=5)

# A ring of lampposts!
place_in_circle(create_lamppost, count=6, radius=5, center_x=0, center_z=5)

cmds.viewFit(allObjects=True)
print("Functions demo complete.")

