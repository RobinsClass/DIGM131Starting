"""
DIGM 131 - Week 7 Demo: Introduction to Classes
=================================================
We'll start with the approach you already know (dicts + functions),
see where it gets awkward, then introduce classes as a cleaner solution.

Run each section one at a time in Maya's Script Editor.
"""

import maya.cmds as cmds

# ============================================================
# PART 1: The Dict + Functions Approach (what you already know)
# ============================================================
# We can represent a "building" as a dictionary and write
# standalone functions that operate on it.

def create_building(name, width=2, height=5, depth=2):
    """Create a building cube and return a dict describing it."""
    cube = cmds.polyCube(w=width, h=height, d=depth, name=name)[0]
    # Lift the cube so its base sits on the ground plane
    cmds.move(0, height / 2.0, 0, cube)
    return {
        "name": cube,
        "width": width,
        "height": height,
        "depth": depth,
        "color": None,
    }

def change_building_color(building, rgb):
    """Apply an RGB color to a building dict's object."""
    shader = cmds.shadingNode("lambert", asShader=True)
    cmds.setAttr(shader + ".color", rgb[0], rgb[1], rgb[2], type="double3")
    cmds.select(building["name"])
    cmds.hyperShade(assign=shader)
    building["color"] = rgb

# Try it out:
b1 = create_building("office_A", width=3, height=8)
change_building_color(b1, (0.4, 0.4, 0.8))

# ---- Friction points with this approach ----
# 1. Nothing ties the functions TO the data -- you could accidentally
#    pass the wrong dict and get a confusing error.
# 2. Every function needs "building" as the first argument.
# 3. If we add Trees, Vehicles, etc., we end up with dozens of
#    loose functions: create_tree, change_tree_color, grow_tree ...
#    It becomes hard to keep track of which function goes with what.


# ============================================================
# PART 2: The Same Thing, But With a Class
# ============================================================
# A class bundles the DATA (attributes) and the FUNCTIONS (methods)
# that operate on that data into one tidy package.

class Building:
    """A simple procedural building in Maya."""

    # __init__ runs automatically when you create a new instance.
    # 'self' is a reference to the specific instance being created.
    def __init__(self, name, width=2, height=5, depth=2):
        # These are INSTANCE ATTRIBUTES -- each Building gets its own copy.
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.color = None
        self.maya_node = None  # will hold the actual Maya object name

    def construct(self):
        """Build the geometry in Maya."""
        cube = cmds.polyCube(
            w=self.width, h=self.height, d=self.depth, name=self.name
        )[0]
        cmds.move(0, self.height / 2.0, 0, cube)
        self.maya_node = cube
        print(f"Constructed {self.maya_node}")

    def demolish(self):
        """Delete the Maya geometry if it exists."""
        if self.maya_node and cmds.objExists(self.maya_node):
            cmds.delete(self.maya_node)
            print(f"Demolished {self.maya_node}")
            self.maya_node = None

    def change_color(self, rgb):
        """Apply an RGB color to this building."""
        if not self.maya_node:
            print("Build the building first with .construct()!")
            return
        shader = cmds.shadingNode("lambert", asShader=True)
        cmds.setAttr(shader + ".color", rgb[0], rgb[1], rgb[2], type="double3")
        cmds.select(self.maya_node)
        cmds.hyperShade(assign=shader)
        self.color = rgb
        print(f"Painted {self.maya_node} -> RGB {rgb}")


# --- Using the Building class ---
tower = Building("tower_01", width=3, height=12, depth=3)
tower.construct()
tower.change_color((0.2, 0.5, 0.9))

house = Building("house_01", width=4, height=3, depth=5)
house.construct()
house.change_color((0.9, 0.8, 0.3))

# Notice how clean this reads compared to the dict approach:
#   tower.change_color(...)   vs   change_building_color(b1, ...)
# The data and behavior live together.


# ============================================================
# PART 3: A Second Class -- Tree
# ============================================================
# Making another class shows how the pattern repeats.

class Tree:
    """A simple stylized tree: sphere canopy on a cylinder trunk."""

    def __init__(self, name, trunk_height=3, canopy_radius=1.5):
        self.name = name
        self.trunk_height = trunk_height
        self.canopy_radius = canopy_radius
        self.trunk_node = None
        self.canopy_node = None

    def plant(self):
        """Create the tree geometry in Maya."""
        # Trunk
        self.trunk_node = cmds.polyCylinder(
            r=0.2, h=self.trunk_height, name=f"{self.name}_trunk"
        )[0]
        cmds.move(0, self.trunk_height / 2.0, 0, self.trunk_node)

        # Canopy (sphere sitting on top of the trunk)
        self.canopy_node = cmds.polySphere(
            r=self.canopy_radius, name=f"{self.name}_canopy"
        )[0]
        cmds.move(0, self.trunk_height + self.canopy_radius * 0.5, 0, self.canopy_node)
        print(f"Planted {self.name}")

    def remove(self):
        """Delete the tree from the scene."""
        for node in (self.trunk_node, self.canopy_node):
            if node and cmds.objExists(node):
                cmds.delete(node)
        self.trunk_node = None
        self.canopy_node = None
        print(f"Removed {self.name}")


# --- Using the Tree class ---
oak = Tree("oak_01", trunk_height=4, canopy_radius=2.5)
oak.plant()

pine = Tree("pine_01", trunk_height=6, canopy_radius=1.0)
pine.plant()
# Move the pine tree over so it doesn't overlap the oak
cmds.move(5, 0, 0, pine.trunk_node, relative=True)
cmds.move(5, 0, 0, pine.canopy_node, relative=True)

# KEY TAKEAWAYS:
# - __init__ sets up the data each instance needs.
# - 'self' is how a method refers to *its own* instance's data.
# - Methods are just functions that live inside the class.
# - Each instance (tower, house, oak, pine) carries its own state.
