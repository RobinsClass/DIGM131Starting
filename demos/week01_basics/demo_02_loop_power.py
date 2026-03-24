"""
DIGM 131 - Week 1 Demo: The Power of Loops
============================================
Run this AFTER demo_01_mel_intro.mel to see the Python version of loops.

Key concepts:
    1. "for i in range(n)" is Python's loop -- no $, no semicolons, no braces
    2. f-strings make naming easy: f"sphere_{i}"
    3. Changing one number (object_count) scales from 5 to 500 objects
    4. Math inside the loop computes positions automatically
"""

import maya.cmds as cmds

# =============================================================================
# SECTION 1: Start fresh
# =============================================================================
cmds.file(new=True, force=True)

# =============================================================================
# SECTION 2: The HARD way -- copy-paste (DO NOT do this!)
# =============================================================================
# The copy-paste approach -- commented out because we'll use a loop instead.

# cmds.polySphere(name="sphere_0", radius=0.5)
# cmds.move(-6, 0.5, 0, "sphere_0")
# cmds.polySphere(name="sphere_1", radius=0.5)
# cmds.move(-3, 0.5, 0, "sphere_1")
# cmds.polySphere(name="sphere_2", radius=0.5)
# cmds.move(0, 0.5, 0, "sphere_2")
# cmds.polySphere(name="sphere_3", radius=0.5)
# cmds.move(3, 0.5, 0, "sphere_3")
# cmds.polySphere(name="sphere_4", radius=0.5)
# cmds.move(6, 0.5, 0, "sphere_4")


# =============================================================================
# SECTION 3: The EASY way -- a for loop
# =============================================================================

object_count = 10       # <-- CHANGE THIS NUMBER live in class!
sphere_radius = 0.5
spacing = 2.5

# Center the row on the origin
start_x = -(object_count - 1) * spacing / 2.0

for i in range(object_count):
    # f-string: Python fills in {i} with the current number
    sphere_name = f"sphere_{i}"

    cmds.polySphere(name=sphere_name, radius=sphere_radius)

    # Compute this sphere's X position using math
    x_position = start_x + i * spacing
    y_position = sphere_radius  # sit on the grid
    cmds.move(x_position, y_position, 0, sphere_name)

print(f"Created {object_count} spheres in a line!")


# =============================================================================
# SECTION 4: Build a staircase -- the real payoff
# =============================================================================

cmds.file(new=True, force=True)

# ---- PARAMETERS -- tweak these live in class! ----
step_count = 12          # how many steps
step_width = 4.0         # how wide each step is (X axis)
step_depth = 1.2         # how deep each step is (Z axis)
step_height = 0.4        # how tall each step rises
step_rotation = 0.0      # degrees to rotate the ENTIRE staircase around Y
# --------------------------------------------------


for i in range(step_count):
    step_name = f"step_{i}"

    # Each step is a box. Its height = all steps up to this one stacked.
    # That way each step is a solid block from the ground up (like real stairs).
    current_height = step_height * (i + 1)

    cmds.polyCube(name=step_name,
                  width=step_width,
                  height=current_height,
                  depth=step_depth)

    # Position: move forward in Z by i * depth, lift Y so base is at ground
    x_pos = 0
    y_pos = current_height / 2.0    # half-height puts the base on Y=0
    z_pos = i * step_depth           # each step is one depth further forward

    cmds.move(x_pos, y_pos, z_pos, step_name)

# Rotate the whole staircase if step_rotation != 0
if step_rotation != 0:
    # Group all steps so we can rotate them together
    all_steps = [f"step_{i}" for i in range(step_count)]
    stair_group = cmds.group(all_steps, name="staircase_grp")
    cmds.rotate(0, step_rotation, 0, stair_group, pivot=[0, 0, 0])

cmds.viewFit(allObjects=True)
print(f"Built a staircase with {step_count} steps!")

# "See how changing ONE variable reshapes the entire thing?
#  That's the power of parameterization."


# =============================================================================
# SECTION 5: Spiral staircase -- rotation inside the loop
# =============================================================================

cmds.file(new=True, force=True)

# ---- PARAMETERS ----
step_count = 24            # more steps for a full spiral
step_width = 3.0           # width of each step
step_depth = 1.5           # depth of each step
step_height = 0.3          # how much each step rises
rotation_per_step = 15.0   # degrees each step turns around center
spiral_radius = 2.5        # how far each step is from the center pole
# --------------------

import math

# Optional: create a center pole
pole_total_height = step_height * step_count
pole = cmds.polyCylinder(name="center_pole",
                         radius=0.2,
                         height=pole_total_height)[0]
cmds.move(0, pole_total_height / 2.0, 0, pole)

for i in range(step_count):
    step_name = f"spiral_step_{i}"

    # Each step is a flat plank
    cmds.polyCube(name=step_name,
                  width=step_width,
                  height=step_height,
                  depth=step_depth)

    # Height: each step sits on top of the previous one
    y_pos = step_height * i + step_height / 2.0

    # Angle: each step rotates a bit more than the last
    angle_degrees = rotation_per_step * i
    angle_radians = math.radians(angle_degrees)

    # Position: offset from center by spiral_radius in the rotated direction
    x_pos = spiral_radius * math.cos(angle_radians)
    z_pos = spiral_radius * math.sin(angle_radians)

    cmds.move(x_pos, y_pos, z_pos, step_name)
    cmds.rotate(0, -angle_degrees, 0, step_name)

    # Color gradient: dark at bottom, light at top
    fraction = i / step_count
    shader_name = f"stepMat_{i}"
    shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
    cmds.setAttr(f"{shader_name}.color",
                 0.3 + 0.5 * fraction,    # red:   dark -> bright
                 0.4 + 0.3 * fraction,    # green: slight shift
                 0.6 + 0.4 * fraction,    # blue:  cool -> warm
                 type="double3")
    cmds.select(step_name)
    cmds.hyperShade(assign=shader)

cmds.viewFit(allObjects=True)
print(f"Built a spiral staircase with {step_count} steps!")


# =============================================================================
# SECTION 6: Rotating the finished staircase as a whole
# =============================================================================

all_spiral_parts = [f"spiral_step_{i}" for i in range(step_count)] + [pole]
spiral_group = cmds.group(all_spiral_parts, name="spiral_staircase_grp")

# Rotate the whole thing 45 degrees
cmds.rotate(0, 45, 0, spiral_group, pivot=[0, 0, 0])


cmds.viewFit(allObjects=True)
print("Rotated the spiral staircase 45 degrees.")


# =============================================================================
# RECAP
# =============================================================================
#   1. for i in range(n):  runs the indented code n times (i = 0, 1, ... n-1)
#   2. f"name_{i}" creates unique names automatically
#   3. Math inside the loop (i * step_height, i * rotation) computes positions
#   4. PARAMETERS at the top control everything -- change one, re-run, done
#   5. Grouping lets you transform many objects as one unit
#   6. "If you're copy-pasting, you need a loop."
