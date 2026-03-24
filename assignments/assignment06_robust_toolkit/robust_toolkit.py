"""
Assignment 6: Robust Toolkit with Error Handling
DIGM 131 - Intro to Scripting for Digital Media

OBJECTIVE:
    Build a small Maya toolkit that handles errors gracefully. You will practice
    try/except blocks, input validation, assertions, and debugging techniques.

REQUIREMENTS:
    1. Implement input validation for ALL functions before performing Maya operations
    2. Wrap every Maya command in a try/except block
    3. Use assertions during development to catch logic errors
    4. Use the DEBUG_MODE flag to control verbose print output
    5. Each function must return a meaningful value (the created object name, True/False, etc.)
    6. Complete the bug report template (bug_report_template.txt) for 3 bugs you encounter

CONCEPTS PRACTICED:
    - try / except / finally
    - Input validation (type checking, range checking)
    - assert statements
    - Debugging with print statements and a debug flag
    - Defensive programming

DELIVERABLES:
    - This file with all TODOs completed
    - bug_report_template.txt with 3 documented bugs

NOTES:
    - Never let your script crash Maya silently. Always give the user feedback.
    - An error message should tell the user WHAT went wrong and HOW to fix it.
"""

import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Debug flag: set to True while developing, False when finished
# When True, functions should print extra information about what they are doing
# ---------------------------------------------------------------------------
DEBUG_MODE = True


def debug_print(message):
    """Print a message only when DEBUG_MODE is True.

    Args:
        message (str): The debug message to print.

    Example:
        debug_print("Created cube with width 5")
    """
    if DEBUG_MODE:
        print("[DEBUG] {}".format(message))


# ---------------------------------------------------------------------------
# EXAMPLE: This function demonstrates the error-handling pattern you should
# follow for every function in this assignment. Study it carefully.
# ---------------------------------------------------------------------------
def create_safe_sphere(name="mySphere", radius=1.0):
    """Create a polygon sphere with full error handling.

    This is a COMPLETED EXAMPLE for you to study. Your functions below
    should follow the same pattern:
        1. Validate inputs
        2. Wrap Maya commands in try/except
        3. Use debug_print for development feedback
        4. Return a useful value or None on failure

    Args:
        name (str): Name for the sphere.
        radius (float): Radius of the sphere. Must be positive.

    Returns:
        str or None: The name of the created sphere, or None if creation failed.
    """
    # --- Step 1: Input validation ---
    if not isinstance(name, str) or len(name) == 0:
        cmds.warning("create_safe_sphere: 'name' must be a non-empty string.")
        return None

    if not isinstance(radius, (int, float)):
        cmds.warning("create_safe_sphere: 'radius' must be a number.")
        return None

    if radius <= 0:
        cmds.warning("create_safe_sphere: 'radius' must be positive. Got {}.".format(radius))
        return None

    # --- Step 2: Assert assumptions (development-time check) ---
    assert isinstance(radius, (int, float)), "radius should be numeric at this point"

    # --- Step 3: Attempt the Maya operation ---
    try:
        result = cmds.polySphere(name=name, radius=radius)
        sphere_name = result[0]
        debug_print("Created sphere '{}' with radius {}".format(sphere_name, radius))
        return sphere_name

    except RuntimeError as e:
        cmds.warning("create_safe_sphere: Maya error - {}".format(e))
        return None

    except Exception as e:
        cmds.warning("create_safe_sphere: Unexpected error - {}".format(e))
        return None


# ---------------------------------------------------------------------------
# YOUR FUNCTIONS: Follow the pattern shown above.
# ---------------------------------------------------------------------------

def create_safe_cube(name="myCube", width=1.0, height=1.0, depth=1.0):
    """Create a polygon cube with input validation and error handling.

    Args:
        name (str): Name for the cube. Must be a non-empty string.
        width (float): Width of the cube. Must be positive.
        height (float): Height of the cube. Must be positive.
        depth (float): Depth of the cube. Must be positive.

    Returns:
        str or None: The name of the created cube, or None if creation failed.
    """
    # TODO: Validate that 'name' is a non-empty string

    # TODO: Validate that width, height, and depth are positive numbers

    # TODO: Add an assertion to confirm your validation logic worked

    # TODO: Wrap cmds.polyCube() in a try/except block
    #   - On success, debug_print the result and return the object name
    #   - On RuntimeError, issue a cmds.warning and return None
    #   - On any other Exception, issue a cmds.warning and return None

    pass


def safe_move(object_name, x=0.0, y=0.0, z=0.0):
    """Move an object to the given position with error handling.

    Args:
        object_name (str): Name of the object to move. Must exist in the scene.
        x (float): X position.
        y (float): Y position.
        z (float): Z position.

    Returns:
        bool: True if the move succeeded, False otherwise.
    """
    # TODO: Validate that object_name is a non-empty string

    # TODO: Check that the object actually exists in the scene
    #   Hint: cmds.objExists(object_name)

    # TODO: Validate that x, y, z are numbers (int or float)

    # TODO: Wrap cmds.move() in a try/except block
    #   - On success, debug_print what you moved and where, return True
    #   - On failure, cmds.warning with a helpful message, return False

    pass


def safe_set_color(object_name, color_index):
    """Set the wireframe color of an object using Maya's color index system.

    Maya color indices range from 0 to 31. This function must validate
    that the index is within that range.

    Args:
        object_name (str): Name of the object. Must exist in the scene.
        color_index (int): Maya color index (0-31).

    Returns:
        bool: True if the color was set successfully, False otherwise.
    """
    # TODO: Validate object_name is a non-empty string and exists in the scene

    # TODO: Validate color_index is an integer in the range 0-31
    #   Hint: use isinstance() and comparison operators

    # TODO: Wrap the color-setting commands in a try/except block
    #   The Maya commands to set wireframe color are:
    #       cmds.setAttr(object_name + ".overrideEnabled", 1)
    #       cmds.setAttr(object_name + ".overrideColor", color_index)
    #   Return True on success, False on failure

    pass


def safe_delete(object_names):
    """Delete one or more objects from the scene safely.

    Args:
        object_names (str or list): A single object name or a list of names.

    Returns:
        int: The number of objects successfully deleted.
    """
    # TODO: If object_names is a single string, convert it to a list
    #   Hint: if isinstance(object_names, str): object_names = [object_names]

    # TODO: Validate that object_names is now a list

    # TODO: Loop through each name in the list
    #   - Check if the object exists before trying to delete it
    #   - Wrap cmds.delete() in a try/except
    #   - Keep a count of how many were successfully deleted
    #   - debug_print each deletion

    # TODO: Return the count of successfully deleted objects

    pass


def batch_create(shape_type, count, spacing=3.0):
    """Create multiple objects in a row with error handling.

    Args:
        shape_type (str): Either "cube" or "sphere".
        count (int): Number of objects to create. Must be between 1 and 50.
        spacing (float): Distance between objects. Must be positive.

    Returns:
        list: A list of names of successfully created objects.
    """
    # TODO: Validate shape_type is either "cube" or "sphere"
    #   Hint: if shape_type not in ("cube", "sphere"):

    # TODO: Validate count is an integer between 1 and 50

    # TODO: Validate spacing is a positive number

    # TODO: Use a loop to create 'count' objects
    #   - Use create_safe_cube or create_safe_sphere depending on shape_type
    #   - Use safe_move to position each object along the X axis
    #   - Collect successfully created names in a list
    #   - If any single creation fails, skip it and continue (don't stop the loop)

    # TODO: debug_print a summary: "Created X of Y requested objects"

    # TODO: Return the list of created object names

    pass


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def main():
    """Main function to demonstrate the robust toolkit.

    TODO: Call each of your functions with both valid and invalid inputs
    to demonstrate that the error handling works. For example:

        # Valid calls
        cube = create_safe_cube("testCube", 2, 3, 2)
        safe_move(cube, 5, 0, 0)

        # Invalid calls (should produce warnings, not crashes)
        create_safe_cube("", -1, 0, 5)
        safe_move("nonexistent_object", 0, 0, 0)
        safe_set_color("testCube", 99)
        safe_delete(12345)
        batch_create("triangle", 100, -5)
    """
    # TODO: Demonstrate valid usage of each function

    # TODO: Demonstrate invalid usage that triggers error handling

    pass


if __name__ == "__main__":
    main()
