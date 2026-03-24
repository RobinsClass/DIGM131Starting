"""
DIGM 131 - Assignment 4: Data-Driven Scene Generator
======================================================

OBJECTIVE:
    Separate your scene DATA from your scene LOGIC. Instead of hard-coding
    every object, you will define scene elements in a data structure (a list
    of dictionaries) and write functions that read that data and build the
    scene automatically.

REQUIREMENTS:
    1. Define a list of dictionaries called SCENE_DATA with at least 10
       entries describing scene elements.
    2. Include at least 3 different element types (e.g., "building",
       "tree", "lamp_post").
    3. Write a function that loops through SCENE_DATA and creates each
       element based on its type and properties.
    4. Follow PEP 8 style: snake_case names, consistent spacing, docstrings.
    5. Adding a new object to the scene should require ONLY adding a new
       dictionary to SCENE_DATA -- no other code changes.

GRADING CRITERIA:
    - [25%] SCENE_DATA contains 10+ entries with 3+ element types.
    - [25%] build_scene() correctly reads data and creates all elements.
    - [20%] create_element() dispatches to the right builder per type.
    - [15%] Adding a new element requires only a new dict in SCENE_DATA.
    - [15%] PEP 8 compliance and thorough commenting.

TIPS:
    - Think of each dict as a "recipe" for one object.
    - Use the "type" key to decide which maya.cmds call to make.
    - You can reuse functions from Assignment 3 if you like.
"""

import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Scene Data
# ---------------------------------------------------------------------------
# Each dictionary describes one element in the scene.
# Keys you should support at minimum: "type", "name", "position".
# Add additional keys as needed for each type (e.g., "width", "height").

SCENE_DATA = [
    {
        "type": "building",
        "name": "office_tower",
        "position": (-10, 0, 5),
        "width": 5,
        "height": 12,
        "depth": 5,
    },
    {
        "type": "tree",
        "name": "oak_tree_01",
        "position": (4, 0, -3),
        "trunk_height": 3,
        "canopy_radius": 2.5,
    },
    {
        "type": "lamp_post",
        "name": "street_lamp_01",
        "position": (8, 0, 0),
        "pole_height": 6,
    },
    # TODO: Add at least 7 more entries to reach the minimum of 10.
    #       Include at least 3 different "type" values total.
    #       Ideas: "fence", "bench", "rock", "vehicle", "sign", etc.
]


# ---------------------------------------------------------------------------
# Builder Functions
# ---------------------------------------------------------------------------

def create_building(data):
    """Create a building element from a data dictionary.

    Args:
        data (dict): Must contain keys "name", "position", and optionally
            "width", "height", "depth".

    Returns:
        str: The name of the created Maya object.
    """
    # TODO: Implement this function.
    #   1. Extract values from 'data', using .get() with sensible defaults.
    #   2. Create a polyCube with those dimensions.
    #   3. Position it so its base sits on the ground.
    #   4. Return the object name.
    pass


def create_tree(data):
    """Create a tree element from a data dictionary.

    Args:
        data (dict): Must contain keys "name", "position", and optionally
            "trunk_height", "canopy_radius".

    Returns:
        str: The name of the created Maya group.
    """
    # TODO: Implement this function.
    pass


def create_lamp_post(data):
    """Create a lamp post element from a data dictionary.

    Args:
        data (dict): Must contain keys "name", "position", and optionally
            "pole_height".

    Returns:
        str: The name of the created Maya group.
    """
    # TODO: Implement this function.
    pass


# TODO: Add builder functions for any additional element types you defined
#       in SCENE_DATA.


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

# This dictionary maps a type name (string) to the function that builds it.
BUILDERS = {
    "building": create_building,
    "tree": create_tree,
    "lamp_post": create_lamp_post,
    # TODO: Add entries for your additional element types.
}


def create_element(data):
    """Create a single scene element by dispatching to the correct builder.

    Looks up data["type"] in the BUILDERS dictionary and calls the
    matching function.

    Args:
        data (dict): A dictionary from SCENE_DATA with at least a "type" key.

    Returns:
        str or None: The object name returned by the builder, or None if
            the type is unrecognized.
    """
    # TODO: Implement this function.
    #   1. Get the element type from data["type"].
    #   2. Look it up in the BUILDERS dict.
    #   3. If found, call the builder function with 'data' and return result.
    #   4. If not found, print a warning and return None.
    pass


def build_scene(scene_data):
    """Build the entire scene by iterating over a list of element dicts.

    Args:
        scene_data (list): A list of dictionaries, each describing one
            scene element.

    Returns:
        list: A list of created object/group names.
    """
    # TODO: Implement this function.
    #   1. Create an empty results list.
    #   2. Loop through each entry in scene_data.
    #   3. Call create_element() for each entry.
    #   4. Append the result to your list (if it is not None).
    #   5. Return the results list.
    pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.file(new=True, force=True)

    # Create a ground plane.
    cmds.polyPlane(name="ground", width=60, height=60,
                   subdivisionsX=1, subdivisionsY=1)

    # Build the scene from data.
    created_objects = build_scene(SCENE_DATA)
    print("Created {} objects: {}".format(len(created_objects), created_objects))

    cmds.viewFit(allObjects=True)
    print("Data-driven scene built successfully!")
