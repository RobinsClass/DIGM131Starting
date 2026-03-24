"""
DIGM 131 - Week 8 Demo: Building Maya UIs
==========================================
Build a tool window step by step using cmds.window, buttons, sliders,
text fields, and option menus.  We keep the LOGIC separate from the
UI code so the tool stays maintainable.
"""

import maya.cmds as cmds
import random

# ============================================================
# PART 1: Logic Functions  (no UI code in here!)
# ============================================================
# Rule of thumb: if a function creates geometry or modifies the
# scene, it should NOT know anything about buttons or sliders.

def create_primitive(prim_type, name, scale=1.0):
    """Create a named primitive of the given type and uniform scale."""
    if prim_type == "Cube":
        node = cmds.polyCube(name=name)[0]
    elif prim_type == "Sphere":
        node = cmds.polySphere(name=name)[0]
    elif prim_type == "Cylinder":
        node = cmds.polyCylinder(name=name)[0]
    else:
        cmds.warning(f"Unknown type: {prim_type}")
        return None
    cmds.scale(scale, scale, scale, node)
    print(f"Created {prim_type} '{node}' at scale {scale}")
    return node


def scatter_selected(count, radius):
    """Duplicate the selected object randomly within a radius."""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Nothing selected -- please select an object first.")
        return
    source = sel[0]
    for i in range(count):
        dup = cmds.duplicate(source, name=f"{source}_scatter_{i+1}")[0]
        x = random.uniform(-radius, radius)
        z = random.uniform(-radius, radius)
        cmds.move(x, 0, z, dup)
    print(f"Scattered {count} copies of '{source}' within radius {radius}")


def delete_all_meshes():
    """Delete every mesh transform in the scene."""
    meshes = cmds.ls(type="mesh")
    if not meshes:
        print("No meshes to delete.")
        return
    transforms = cmds.listRelatives(meshes, parent=True, fullPath=True) or []
    transforms = list(set(transforms))  # remove duplicates
    cmds.delete(transforms)
    print(f"Deleted {len(transforms)} mesh object(s).")


# ============================================================
# PART 2: UI Callback Functions
# ============================================================
# Callbacks are the BRIDGE between UI widgets and logic functions.
# They read values from UI controls and pass them to logic functions.
# Maya passes an extra argument to button callbacks (*args catches it).

# We store the window name so we can delete it if it already exists.
WINDOW_NAME = "primitiveToolWin"


def on_create_clicked(*args):
    """Called when the 'Create' button is pressed."""
    # Query current values from UI controls
    prim_type = cmds.optionMenu(widgets["type_menu"], q=True, value=True)
    name = cmds.textField(widgets["name_field"], q=True, text=True) or "myPrim"
    scale = cmds.floatSliderGrp(widgets["scale_slider"], q=True, value=True)
    create_primitive(prim_type, name, scale)


def on_scatter_clicked(*args):
    """Called when the 'Scatter' button is pressed."""
    count = int(cmds.intSliderGrp(widgets["count_slider"], q=True, value=True))
    radius = cmds.floatSliderGrp(widgets["radius_slider"], q=True, value=True)
    scatter_selected(count, radius)


def on_delete_clicked(*args):
    """Called when the 'Delete All' button is pressed."""
    delete_all_meshes()


# ============================================================
# PART 3: Building the Window
# ============================================================
# We keep a dict of widget names so callbacks can query them.
widgets = {}


def build_ui():
    """Create and show the tool window."""
    # If the window already exists, delete it first to avoid duplicates.
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    cmds.window(WINDOW_NAME, title="Primitive Tool", widthHeight=(380, 300))

    # A columnLayout stacks widgets vertically with some padding.
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=("both", 10))

    # --- Section: Create Primitive ---
    cmds.separator(height=10, style="none")
    cmds.text(label="--- Create Primitive ---", align="center", font="boldLabelFont")

    # Option menu (dropdown) for primitive type
    widgets["type_menu"] = cmds.optionMenu(label="Type: ")
    cmds.menuItem(label="Cube")
    cmds.menuItem(label="Sphere")
    cmds.menuItem(label="Cylinder")

    # Text field for object name
    cmds.text(label="Name:", align="left")
    widgets["name_field"] = cmds.textField(text="myPrim")

    # Float slider for scale
    widgets["scale_slider"] = cmds.floatSliderGrp(
        label="Scale: ", field=True,
        minValue=0.1, maxValue=10.0, value=1.0
    )

    # Create button -- connects to our callback
    cmds.button(label="Create", command=on_create_clicked,
                backgroundColor=(0.4, 0.7, 0.4))

    # --- Section: Scatter Tool ---
    cmds.separator(height=12, style="in")
    cmds.text(label="--- Scatter Selected ---", align="center", font="boldLabelFont")

    widgets["count_slider"] = cmds.intSliderGrp(
        label="Count: ", field=True,
        minValue=1, maxValue=50, value=5
    )
    widgets["radius_slider"] = cmds.floatSliderGrp(
        label="Radius: ", field=True,
        minValue=1.0, maxValue=50.0, value=10.0
    )

    cmds.button(label="Scatter Selected", command=on_scatter_clicked,
                backgroundColor=(0.4, 0.5, 0.8))

    # --- Section: Cleanup ---
    cmds.separator(height=12, style="in")
    cmds.button(label="Delete All Meshes", command=on_delete_clicked,
                backgroundColor=(0.8, 0.3, 0.3))

    cmds.separator(height=10, style="none")

    # Show the window
    cmds.showWindow(WINDOW_NAME)
    print("Primitive Tool window opened.")


# ============================================================
# RUN
# ============================================================
build_ui()

# KEY TAKEAWAYS:
# - Logic functions know NOTHING about UI widgets.
# - Callbacks are thin -- they read widgets and call logic functions.
# - This separation means you can test the logic without the UI,
#   and redesign the UI without rewriting the logic.
