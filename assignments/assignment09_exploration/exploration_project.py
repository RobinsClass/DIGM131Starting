"""
Assignment 9: Exploration Project
DIGM 131 - Intro to Scripting for Digital Media

OBJECTIVE:
    Choose a Maya scripting domain you have NOT worked with before and build
    a small tool or script that demonstrates what you learned. This assignment
    is about independent learning and research.

CHOOSE ONE DOMAIN (or propose your own):
    - Animation: set keyframes, create motion paths, animate attributes
    - Materials/Shading: create and assign materials, set shader attributes
    - Curves and Surfaces: NURBS curves, lofts, extrudes along paths
    - Particle Effects: emitters, particle attributes, fields
    - Rigging Basics: joints, IK handles, constraints
    - Rendering: cameras, lights, render settings
    - Deformers: bend, twist, lattice, blend shapes

REQUIREMENTS:
    1. Pick a domain from the list above (or propose one to the instructor)
    2. Research at least 5 Maya commands related to your domain
    3. Write a script that uses those commands to create something
    4. Include error handling (try/except) for all Maya commands
    5. Complete the learning_log_template.txt for each command you explored
    6. Complete the peer_review_template.txt for a classmate's project

DELIVERABLES:
    - This file with your exploration code
    - learning_log_template.txt filled out (at least 5 entries)
    - peer_review_template.txt filled out for a classmate

GRADING:
    - Code functionality: 30%
    - Research depth (learning log): 30%
    - Code quality and documentation: 20%
    - Peer review quality: 20%

LEARNING LOG TEMPLATE (also in learning_log_template.txt):
    For each command you explored, document:
    - Command explored:       (e.g., cmds.shadingNode)
    - What I searched for:    (e.g., "maya python create material")
    - What confused me:       (e.g., "difference between shader and shading group")
    - How I figured it out:   (e.g., "Maya docs example + Stack Overflow post")
    - Performance notes:      (e.g., "slow with 1000+ objects, had to batch")
"""

import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Domain: (TODO: Write which domain you chose here)
# ---------------------------------------------------------------------------

# TODO: Write your exploration code below.
#
# Structure suggestion:
#   1. A few helper functions for the new commands you learned
#   2. A main function that uses those helpers to create something
#   3. Error handling around every new Maya command
#
# Example structure (for a Materials exploration):
#
#   def create_material(name, color):
#       """Create a Lambert material with the given color.
#
#       Args:
#           name (str): Name for the material.
#           color (tuple): RGB color as (r, g, b), values 0.0 to 1.0.
#
#       Returns:
#           str or None: The material name, or None on failure.
#       """
#       try:
#           mat = cmds.shadingNode("lambert", asShader=True, name=name)
#           cmds.setAttr(mat + ".color", color[0], color[1], color[2], type="double3")
#           return mat
#       except Exception as e:
#           cmds.warning("Failed to create material: {}".format(e))
#           return None
#
#
#   def assign_material(material_name, object_name):
#       ...
#
#
#   def main():
#       red_mat = create_material("redMaterial", (1, 0, 0))
#       cube = cmds.polyCube(name="coloredCube")[0]
#       assign_material(red_mat, cube)
#       print("Exploration complete!")


def main():
    """Entry point for the exploration project."""
    # TODO: Your main code here
    pass


if __name__ == "__main__":
    main()
