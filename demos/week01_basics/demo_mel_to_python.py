"""
DIGM 131 - Week 1 Demo: MEL to Python Transition
==================================================
    Before running this script, open Maya's Script Editor (Windows > General Editors > Script Editor).
    Show students the MEL tab first. Create a cube via the menu (Create > Polygon Primitives > Cube).
    Point out the MEL feedback in the Script Editor:
        polyCube -w 1 -h 1 -d 1 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1;
    Then switch to the Python tab and explain: "Every MEL command has a Python equivalent in maya.cmds."
"""

import maya.cmds as cmds

# =============================================================================
# SECTION 1: The import statement
# =============================================================================
# The 'as cmds' part creates a short alias so we don't have to type 'maya.cmds' every time.
# This single line is at the top of EVERY Maya Python script we will write in this course.

# =============================================================================
# SECTION 2: MEL vs Python — Creating primitives
# =============================================================================
# MEL:    polyCube -name "myBox" -width 2 -height 3 -depth 2;
# Python:
cmds.polyCube(name="myBox", width=2, height=3, depth=2)


# Let's create a sphere the same way.
# MEL:    polySphere -name "mySphere" -radius 1.5;
# Python:
cmds.polySphere(name="mySphere", radius=1.5)

# And a cylinder.
# MEL:    polyCylinder -name "myCylinder" -radius 0.5 -height 4;
# Python:
cmds.polyCylinder(name="myCylinder", radius=0.5, height=4)

# =============================================================================
# SECTION 3: Moving, rotating, and scaling — the big three transforms
# =============================================================================
# In Python we use cmds.move() or cmds.xform(). Let's start with the simple versions.

# Move the box 3 units along X
cmds.move(3, 0, 0, "myBox")

# Rotate the sphere 45 degrees around Y
cmds.rotate(0, 45, 0, "mySphere")

# Scale the cylinder to be twice as wide
cmds.scale(2, 1, 2, "myCylinder")

# This matches Maya's coordinate system: X = left/right, Y = up/down, Z = front/back.

# =============================================================================
# SECTION 4: Variables — giving values descriptive names
# =============================================================================

# Instead of magic numbers, store values in well-named variables.
box_x_position = 5.0
box_y_position = 1.5
box_z_position = -2.0

# Now use those variables to position our box.
cmds.move(box_x_position, box_y_position, box_z_position, "myBox")


# Variables for object dimensions
tower_width = 1.0
tower_height = 8.0
tower_depth = 1.0

tower = cmds.polyCube(name="tower", width=tower_width, height=tower_height, depth=tower_depth)
# The first element is the transform node name, the second is the construction history node.
print("polyCube returned:", tower)

# Place the tower so its base sits on the grid (Y=0). We need to lift it by half its height.
tower_y_offset = tower_height / 2.0
cmds.move(0, tower_y_offset, 0, tower[0])

# =============================================================================
# SECTION 5: Basic math with variables
# =============================================================================

# Spacing objects evenly along a line
spacing = 3.0
start_x = -6.0

# Create three spheres and space them out using math
sphere_a = cmds.polySphere(name="sphereA", radius=0.5)[0]
sphere_b = cmds.polySphere(name="sphereB", radius=0.5)[0]
sphere_c = cmds.polySphere(name="sphereC", radius=0.5)[0]

cmds.move(start_x, 0, 0, sphere_a)
cmds.move(start_x + spacing, 0, 0, sphere_b)          # -6 + 3 = -3
cmds.move(start_x + spacing * 2, 0, 0, sphere_c)      # -6 + 6 =  0

# Multiplication (*) happens before addition (+), just like regular math.
# If unsure, use parentheses: start_x + (spacing * 2)

# Let's compute a total height from parts
base_height = 1.0
column_height = 5.0
cap_height = 0.5
total_height = base_height + column_height + cap_height
print("Total structure height:", total_height)  # 6.5

# =============================================================================
# SECTION 6: Querying attributes — reading back from the scene
# =============================================================================
# This is the Python version of MEL's: getAttr "myBox.translateX";

box_tx = cmds.getAttr("myBox.translateX")
box_ty = cmds.getAttr("myBox.translateY")
box_tz = cmds.getAttr("myBox.translateZ")
print("myBox position: X={}, Y={}, Z={}".format(box_tx, box_ty, box_tz))

# "From here on out, we will work entirely in Python."
