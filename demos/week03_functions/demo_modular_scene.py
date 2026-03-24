"""
DIGM 131 - Week 3 Demo: Modular Scene Composition
===================================================
    This demo shows how small, focused functions compose together to build a complex
    scene. Each function does ONE thing (Single Responsibility Principle). Return values
    chain from one function into the next. The final scene is built by calling high-level
    functions that internally use low-level ones.
    Run in Maya's Script Editor (Python tab).
"""

import maya.cmds as cmds
import math

cmds.file(new=True, force=True)

# =============================================================================
# SECTION 1: Low-level creation functions (each does ONE thing)
# =============================================================================
# a function should do one thing and do it well."

def create_ground(width=40, depth=40):
    """Create and shade a ground plane. Returns the ground node name."""
    ground = cmds.polyPlane(name="ground", width=width, height=depth,
                            subdivisionsX=1, subdivisionsY=1)[0]
    shader = cmds.shadingNode("lambert", asShader=True, name="groundShader")
    cmds.setAttr(shader + ".color", 0.35, 0.45, 0.3, type="double3")
    cmds.select(ground)
    cmds.hyperShade(assign=shader)
    return ground


def create_building(x, z, width=2.0, height=5.0, depth=2.0):
    """Create a single building at (x, z). Returns the building node name."""
    bldg = cmds.polyCube(width=width, height=height, depth=depth)[0]
    cmds.move(x, height / 2.0, z, bldg)
    return bldg


def create_tree(x, z, trunk_height=2.0, canopy_radius=1.0):
    """Create a tree (trunk + canopy) at (x, z). Returns (trunk, canopy) node names."""
    trunk = cmds.polyCylinder(radius=0.25, height=trunk_height)[0]
    cmds.move(x, trunk_height / 2.0, z, trunk)
    canopy = cmds.polySphere(radius=canopy_radius)[0]
    cmds.move(x, trunk_height + canopy_radius * 0.5, z, canopy)
    return trunk, canopy


def create_lamppost(x, z, height=3.0):
    """Create a lamppost (pole + lamp) at (x, z). Returns (pole, lamp) node names."""
    pole = cmds.polyCylinder(radius=0.08, height=height)[0]
    cmds.move(x, height / 2.0, z, pole)
    lamp = cmds.polySphere(radius=0.2)[0]
    cmds.move(x, height + 0.2, z, lamp)
    return pole, lamp


def create_bench(x, z, rotation_y=0):
    """Create a simple bench (seat + two legs). Returns a group node."""
    seat = cmds.polyCube(width=1.5, height=0.1, depth=0.5)[0]
    cmds.move(x, 0.5, z, seat)
    leg_l = cmds.polyCube(width=0.1, height=0.5, depth=0.4)[0]
    cmds.move(x - 0.6, 0.25, z, leg_l)
    leg_r = cmds.polyCube(width=0.1, height=0.5, depth=0.4)[0]
    cmds.move(x + 0.6, 0.25, z, leg_r)
    grp = cmds.group(seat, leg_l, leg_r, name="bench_grp#")
    cmds.rotate(0, rotation_y, 0, grp, pivot=(x, 0, z))
    return grp

# =============================================================================
# SECTION 2: Mid-level composition functions — combining creation with layout
# =============================================================================
# Notice how each mid-level function focuses on LAYOUT, not geometry details."

def build_city_block(center_x, center_z, building_count=4):
    """Place a cluster of buildings with varied heights around a center point.
    Returns a list of building node names."""
    buildings = []
    for i in range(building_count):
        # Spread buildings in a small area around the center
        angle = (2 * math.pi / building_count) * i
        offset = 2.5
        bx = center_x + math.cos(angle) * offset
        bz = center_z + math.sin(angle) * offset
        # Vary the height so the skyline looks interesting
        height = 3.0 + (i * 2.5)
        bldg = create_building(bx, bz, width=1.8, height=height, depth=1.8)
        buildings.append(bldg)
    return buildings


def build_park(center_x, center_z, tree_count=6, radius=5.0):
    """Arrange trees in a circle to form a small park. Returns lists of nodes."""
    trunks = []
    canopies = []
    for i in range(tree_count):
        angle = (2 * math.pi / tree_count) * i
        tx = center_x + math.cos(angle) * radius
        tz = center_z + math.sin(angle) * radius
        trunk, canopy = create_tree(tx, tz)
        trunks.append(trunk)
        canopies.append(canopy)
    return trunks, canopies


def line_street_with_lampposts(start_x, end_x, z, spacing=4.0):
    """Place lampposts along a line from start_x to end_x at the given z.
    Returns a list of (pole, lamp) tuples."""
    posts = []
    x = start_x
    while x <= end_x:
        post = create_lamppost(x, z)
        posts.append(post)
        x += spacing
    return posts

# =============================================================================
# SECTION 3: Shading utility — apply color to a list of objects
# =============================================================================
# This function takes any list of nodes and colors them all the same way."

def apply_color(nodes, r, g, b, shader_name="colorShader"):
    """Apply a Lambert shader with the given RGB color to all listed nodes."""
    shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
    cmds.setAttr(shader + ".color", r, g, b, type="double3")
    for node in nodes:
        cmds.select(node)
        cmds.hyperShade(assign=shader)
    return shader

# =============================================================================
# SECTION 4: Top-level scene assembly — the "main" function
# =============================================================================
# Each line is a high-level instruction; the details are hidden inside each function."

def build_full_scene():
    """Assemble the complete scene from modular parts."""

    # 1. Ground
    create_ground(width=50, depth=50)

    # 2. Two city blocks
    block_a = build_city_block(center_x=-8, center_z=-6, building_count=5)
    block_b = build_city_block(center_x=8, center_z=-6, building_count=4)
    apply_color(block_a, 0.55, 0.55, 0.65, shader_name="buildingsA_mat")
    apply_color(block_b, 0.6, 0.5, 0.45, shader_name="buildingsB_mat")

    # 3. A park in the front of the scene
    trunks, canopies = build_park(center_x=0, center_z=6, tree_count=8, radius=5)
    apply_color(trunks, 0.4, 0.25, 0.1, shader_name="trunkMat")
    apply_color(canopies, 0.2, 0.55, 0.2, shader_name="canopyMat")

    # 4. Street lamps between the two city blocks
    posts = line_street_with_lampposts(start_x=-12, end_x=12, z=-2, spacing=4)
    poles = [p for p, l in posts]
    lamps = [l for p, l in posts]
    apply_color(poles, 0.25, 0.25, 0.25, shader_name="poleMat")
    apply_color(lamps, 1.0, 0.95, 0.6, shader_name="lampMat")

    # 5. A few benches in the park
    create_bench(-2, 6, rotation_y=30)
    create_bench(2, 6, rotation_y=-30)
    create_bench(0, 9, rotation_y=0)

    # Frame the viewport
    cmds.viewFit(allObjects=True)
    print("Modular scene built successfully.")


# If you want to change how a tree looks, you edit create_tree() in ONE place.
# If you want more buildings, you just call build_city_block() again."
build_full_scene()

