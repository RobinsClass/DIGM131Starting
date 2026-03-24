"""
DIGM 131 - Week 1 Demo: Building a Simple Scene
=================================================
    This demo builds a small cityscape step by step: a ground plane, several buildings,
    and a few trees. Every measurement is stored in a well-named variable so students
    see the value of descriptive naming from day one.
    Run this script in Maya's Script Editor (Python tab) or via the shelf.
    Encourage students to tweak the variables and re-run to see changes.
"""

import maya.cmds as cmds

# =============================================================================
# SECTION 1: Start with a clean scene
# =============================================================================
# The force=True flag skips the "Save changes?" dialog.
cmds.file(new=True, force=True)

# =============================================================================
# SECTION 2: Create the ground plane
# =============================================================================
ground_width = 30
ground_depth = 30

ground = cmds.polyPlane(name="ground", width=ground_width, height=ground_depth,
                        subdivisionsX=1, subdivisionsY=1)[0]

# Give the ground a dark grey color using a Lambert shader
ground_shader = cmds.shadingNode("lambert", asShader=True, name="groundMat")
cmds.setAttr(ground_shader + ".color", 0.3, 0.3, 0.3, type="double3")
cmds.select(ground)
cmds.hyperShade(assign=ground_shader)

# We will cover shaders more later; for now just notice the pattern:
#   1. Create a shader node   2. Set its color   3. Assign it to an object

# =============================================================================
# SECTION 3: Build some buildings (cubes with different heights)
# =============================================================================

# --- Building A: a tall narrow tower ---
building_a_width = 2
building_a_height = 8
building_a_depth = 2
building_a_x = -5
building_a_z = -3

building_a = cmds.polyCube(name="buildingA",
                           width=building_a_width,
                           height=building_a_height,
                           depth=building_a_depth)[0]
# Lift the building so its base sits on the ground (Y = half its height)
cmds.move(building_a_x, building_a_height / 2.0, building_a_z, building_a)

# --- Building B: a wide, shorter office block ---
building_b_width = 5
building_b_height = 4
building_b_depth = 3
building_b_x = 3
building_b_z = -4

building_b = cmds.polyCube(name="buildingB",
                           width=building_b_width,
                           height=building_b_height,
                           depth=building_b_depth)[0]
cmds.move(building_b_x, building_b_height / 2.0, building_b_z, building_b)

# --- Building C: a medium apartment building ---
building_c_width = 3
building_c_height = 6
building_c_depth = 3
building_c_x = -2
building_c_z = 4

building_c = cmds.polyCube(name="buildingC",
                           width=building_c_width,
                           height=building_c_height,
                           depth=building_c_depth)[0]
cmds.move(building_c_x, building_c_height / 2.0, building_c_z, building_c)

# "See how we keep doing the same steps? Next week we'll learn to avoid this repetition."

# Apply a building shader — blue-grey concrete look
building_shader = cmds.shadingNode("lambert", asShader=True, name="buildingMat")
cmds.setAttr(building_shader + ".color", 0.5, 0.55, 0.65, type="double3")
for bldg in [building_a, building_b, building_c]:
    cmds.select(bldg)
    cmds.hyperShade(assign=building_shader)

# =============================================================================
# SECTION 4: Create some trees (cylinder trunk + sphere canopy)
# =============================================================================
# and a green sphere for the leaves."

# --- Tree 1 ---
tree1_x = 6
tree1_z = 3
trunk_radius = 0.3
trunk_height = 2.0
canopy_radius = 1.2

trunk1 = cmds.polyCylinder(name="trunk1", radius=trunk_radius, height=trunk_height)[0]
cmds.move(tree1_x, trunk_height / 2.0, tree1_z, trunk1)

canopy1 = cmds.polySphere(name="canopy1", radius=canopy_radius)[0]
# The canopy sits on top of the trunk
canopy_y = trunk_height + canopy_radius * 0.6  # slight overlap looks more natural
cmds.move(tree1_x, canopy_y, tree1_z, canopy1)

# --- Tree 2 — reuse the same size variables, different position ---
tree2_x = 8
tree2_z = -1

trunk2 = cmds.polyCylinder(name="trunk2", radius=trunk_radius, height=trunk_height)[0]
cmds.move(tree2_x, trunk_height / 2.0, tree2_z, trunk2)

canopy2 = cmds.polySphere(name="canopy2", radius=canopy_radius)[0]
cmds.move(tree2_x, canopy_y, tree2_z, canopy2)

# --- Tree 3 ---
tree3_x = -8
tree3_z = 0

trunk3 = cmds.polyCylinder(name="trunk3", radius=trunk_radius, height=trunk_height)[0]
cmds.move(tree3_x, trunk_height / 2.0, tree3_z, trunk3)

canopy3 = cmds.polySphere(name="canopy3", radius=canopy_radius)[0]
cmds.move(tree3_x, canopy_y, tree3_z, canopy3)

# In week 3 we'll write a create_tree() function to eliminate this repetition."

# Trunk shader — brown
trunk_shader = cmds.shadingNode("lambert", asShader=True, name="trunkMat")
cmds.setAttr(trunk_shader + ".color", 0.4, 0.25, 0.1, type="double3")
for trunk in [trunk1, trunk2, trunk3]:
    cmds.select(trunk)
    cmds.hyperShade(assign=trunk_shader)

# Canopy shader — green
canopy_shader = cmds.shadingNode("lambert", asShader=True, name="canopyMat")
cmds.setAttr(canopy_shader + ".color", 0.15, 0.5, 0.15, type="double3")
for canopy in [canopy1, canopy2, canopy3]:
    cmds.select(canopy)
    cmds.hyperShade(assign=canopy_shader)

# =============================================================================
# SECTION 5: Frame the scene in the viewport
# =============================================================================
cmds.viewFit(allObjects=True)

print("Scene complete! Ground, 3 buildings, and 3 trees created.")
