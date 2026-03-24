"""
DIGM 131 - Week 9 Demo: How to Read Maya Python Documentation
==============================================================
This is a GUIDED EXERCISE.  Follow along in your browser with the
Maya Python Command Reference open:
  https://help.autodesk.com/cloudhelp/2025/ENU/Maya-Tech-Docs/CommandsPython/

Learning to read documentation is one of the most important skills
you can develop.  Let's practice.
"""

import maya.cmds as cmds

# ============================================================
# STEP 1: Anatomy of a Doc Page
# ============================================================
# Open the docs for cmds.polyCube.  You'll see these sections:
#   Synopsis   -- one-line summary of what the command does.
#   Return     -- what the command gives back (e.g., list of strings).
#   Flags      -- the keyword arguments you can pass.
#                 Each flag shows:
#                   - long name (e.g., 'width') and short name ('w')
#                   - data type (e.g., float, int, string)
#                   - whether it's queryable (q=True) or editable (e=True)
#   Examples   -- sample MEL/Python code at the bottom of the page.

# KEY INSIGHT: Almost every cmds function has three modes:
#   CREATE mode  -->  cmds.polyCube(width=3)
#   QUERY mode   -->  cmds.polyCube("pCube1", q=True, width=True)
#   EDIT mode    -->  cmds.polyCube("pCube1", e=True, width=5)


# ============================================================
# EXERCISE 1: cmds.polySphere
# ============================================================
# TASK: Look up cmds.polySphere in the docs.
#   a) What flag controls the number of horizontal subdivisions?
#   b) Create a sphere with 32 subdivisions on each axis.
#   c) Query the radius of the sphere you just created.

# --- YOUR ATTEMPT HERE ---


# --- SOLUTION ---
# a) 'subdivisionsAxis' (short: 'sa') for horizontal,
#    'subdivisionsHeight' (short: 'sh') for vertical.
# b)
my_sphere = cmds.polySphere(
    name="doc_sphere",
    subdivisionsAxis=32,
    subdivisionsHeight=32,
)[0]
# c)
r = cmds.polySphere(my_sphere, q=True, radius=True)
print(f"Radius of {my_sphere}: {r}")


# ============================================================
# EXERCISE 2: cmds.polyBevel (or polyBevel3)
# ============================================================
# TASK: Look up cmds.polyBevel3.
#   a) What flag sets the bevel width (offset)?
#   b) What flag controls how many segments the bevel has?
#   c) Create a cube, select it, and apply a bevel with
#      offset=0.3 and segments=3.

# --- YOUR ATTEMPT HERE ---


# --- SOLUTION ---
# a) 'offset' (short: 'o')
# b) 'segments' (short: 'sg')
# c)
bevel_cube = cmds.polyCube(name="bevel_cube")[0]
cmds.select(bevel_cube)
cmds.polyBevel3(
    bevel_cube,
    offset=0.3,
    segments=3,
    fraction=0.5,
)
print(f"Beveled {bevel_cube} with offset=0.3, segments=3")


# ============================================================
# EXERCISE 3: cmds.xform  (a big, important command)
# ============================================================
# TASK: Look up cmds.xform.
#   a) How do you query the WORLD-SPACE position of an object?
#   b) How do you set the pivot point?
#   c) Query the world-space bounding box of bevel_cube.

# --- YOUR ATTEMPT HERE ---


# --- SOLUTION ---
# a) cmds.xform(obj, q=True, worldSpace=True, translation=True)
pos = cmds.xform(bevel_cube, q=True, ws=True, t=True)
print(f"World position: {pos}")

# b) cmds.xform(obj, pivots=[x, y, z])
cmds.xform(bevel_cube, pivots=[0, -0.5, 0])

# c) cmds.xform(obj, q=True, boundingBox=True)  -> [xmin,ymin,zmin,xmax,ymax,zmax]
bb = cmds.xform(bevel_cube, q=True, bb=True)
print(f"Bounding box: {bb}")


# ============================================================
# EXERCISE 4: Finding Commands You Don't Know Yet
# ============================================================
# Sometimes you don't know the command name.  Strategies:
#   1. Search the docs page (Ctrl+F) for keywords like "smooth",
#      "duplicate", "curve", etc.
#   2. Google: "maya python cmds smooth mesh"
#   3. In Maya's Script Editor, do something with the menus and
#      watch the MEL output -- then look up the Python equivalent.
# TASK: Figure out how to smooth a mesh in Python.
# HINT: Try searching for "polySmooth" in the docs.

# --- SOLUTION ---
smooth_cube = cmds.polyCube(name="smooth_cube")[0]
cmds.polySmooth(smooth_cube, divisions=2)
print(f"Smoothed {smooth_cube} with 2 divisions")


# ============================================================
# TIPS FOR READING ANY API DOCS (not just Maya)
# ============================================================
# 1. Read the RETURN VALUE first -- what do you get back?
# 2. Scan the FLAGS/PARAMETERS list -- you don't need all of them,
#    just find the ones relevant to your task.
# 3. Look at the EXAMPLES at the bottom -- they're gold.
# 4. Try it in the Script Editor interactively before putting
#    it in your script.
# 5. Use Python's help():  help(cmds.polyBevel3)
