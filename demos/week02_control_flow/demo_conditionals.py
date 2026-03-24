"""
DIGM 131 - Week 2 Demo: Conditionals in Maya
==============================================
    This demo teaches if/elif/else using Maya scene queries. We create objects,
    read their attributes with getAttr, and make decisions: coloring objects
    based on height, checking positions, and combining conditions with logical operators.
    Run in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds

# Start fresh
cmds.file(new=True, force=True)

# =============================================================================
# SECTION 1: Simple if/else — Is a value above a threshold?
# =============================================================================
# and runs the indented code only if the condition is True."

# Create a tall cube
tower_height = 7.0
tower = cmds.polyCube(name="tower", height=tower_height, width=1.5, depth=1.5)[0]
cmds.move(0, tower_height / 2.0, 0, tower)

# Query the height back from the scene to demonstrate getAttr
actual_height = cmds.getAttr(tower + ".scaleY") * tower_height
print("Tower height:", actual_height)

if actual_height > 5.0:
    print("This tower is TALL (over 5 units).")
else:
    print("This tower is SHORT (5 units or under).")

# =============================================================================
# SECTION 2: if / elif / else — Multiple categories
# =============================================================================

# Create several cubes at different heights and color them by category
height_list = [2.0, 5.0, 8.0, 12.0]

# We'll need shaders for three height categories
short_shader = cmds.shadingNode("lambert", asShader=True, name="shortMat")
cmds.setAttr(short_shader + ".color", 0.2, 0.7, 0.2, type="double3")  # green

medium_shader = cmds.shadingNode("lambert", asShader=True, name="mediumMat")
cmds.setAttr(medium_shader + ".color", 0.9, 0.7, 0.1, type="double3")  # yellow

tall_shader = cmds.shadingNode("lambert", asShader=True, name="tallMat")
cmds.setAttr(tall_shader + ".color", 0.8, 0.15, 0.15, type="double3")  # red

for i, h in enumerate(height_list):
    cube_name = "building_{}".format(i)
    cube = cmds.polyCube(name=cube_name, height=h, width=1.5, depth=1.5)[0]
    x_pos = -4.5 + i * 3.0  # space them out along X
    cmds.move(x_pos, h / 2.0, 0, cube)

    # Decide which shader to apply based on height
    if h < 4.0:
        # Short building — green
        chosen_shader = short_shader
        label = "short"
    elif h < 9.0:
        # Medium building — yellow
        chosen_shader = medium_shader
        label = "medium"
    else:
        # Tall building — red
        chosen_shader = tall_shader
        label = "tall"

    cmds.select(cube)
    cmds.hyperShade(assign=chosen_shader)
    print("{} is {} (height={})".format(cube_name, label, h))

# then it skips the rest. Order matters!"

# =============================================================================
# SECTION 3: Comparison operators review
# =============================================================================

# Demonstrate with getAttr — query an object's X position
obj_x = cmds.getAttr("building_0.translateX")
print("building_0 is at X =", obj_x)

if obj_x < 0:
    print("building_0 is on the LEFT side of the scene (negative X).")
elif obj_x == 0:
    print("building_0 is at the CENTER.")
else:
    print("building_0 is on the RIGHT side (positive X).")

# =============================================================================
# SECTION 4: Logical operators — and, or, not
# =============================================================================

# Create a sphere and check multiple properties at once
test_sphere = cmds.polySphere(name="testSphere", radius=1.0)[0]
cmds.move(3, 6, 0, test_sphere)

sphere_x = cmds.getAttr(test_sphere + ".translateX")
sphere_y = cmds.getAttr(test_sphere + ".translateY")

# AND — both must be True
if sphere_x > 0 and sphere_y > 5:
    print("Sphere is in the upper-right area of the scene.")

# OR — at least one must be True
if sphere_x > 10 or sphere_y > 10:
    print("Sphere is far from the origin on at least one axis.")
else:
    print("Sphere is reasonably close to the origin.")

# NOT — flips True/False
is_visible = cmds.getAttr(test_sphere + ".visibility")
if not is_visible:
    print("The sphere is hidden!")
else:
    print("The sphere is visible.")

# =============================================================================
# SECTION 5: Practical example — tag objects by position quadrant
# =============================================================================
# and print which quadrant of the ground it's in."

all_buildings = ["building_0", "building_1", "building_2", "building_3"]

for bldg in all_buildings:
    bx = cmds.getAttr(bldg + ".translateX")
    bz = cmds.getAttr(bldg + ".translateZ")

    # Determine quadrant using nested conditions
    if bx >= 0 and bz >= 0:
        quadrant = "front-right"
    elif bx < 0 and bz >= 0:
        quadrant = "front-left"
    elif bx < 0 and bz < 0:
        quadrant = "back-left"
    else:
        quadrant = "back-right"

    print("{} is in the {} quadrant".format(bldg, quadrant))

# Frame everything nicely
cmds.viewFit(allObjects=True)

