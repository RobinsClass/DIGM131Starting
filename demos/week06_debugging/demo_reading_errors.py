"""
DIGM 131 - Week 6 Demo: Reading Error Messages
================================================
This file contains INTENTIONALLY BROKEN code.

Each section triggers a different Python error type.
Read the comments to understand what went wrong and why.

HOW TO USE THIS DEMO:
  1. Uncomment ONE section at a time in run_demo().
  2. Run the script in Maya's Script Editor.
  3. Read the error message in the output.
  4. Try to fix it before looking at the explanation.
"""

import maya.cmds as cmds


# ===================================================================
# BUG 1: NameError
# "NameError: name 'cubee' is not defined"
# Cause: A typo in a variable name.  Python is case-sensitive and
#        checks spelling exactly.
# Fix:   Change 'cubee' to 'cube'.
# ===================================================================
def bug_name_error():
    cube = cmds.polyCube(name="test_cube")[0]
    # Oops -- 'cubee' is not defined, we meant 'cube'
    cmds.move(0, 3, 0, cubee)  # noqa: F821  -- intentional bug


# ===================================================================
# BUG 2: TypeError
# "TypeError: polyCube() got an unexpected keyword argument 'hight'"
# Cause: Misspelled keyword argument.  The correct name is 'height'.
# Fix:   Change 'hight' to 'height'.
# ===================================================================
def bug_type_error():
    # 'hight' is not a valid parameter -- should be 'height'
    cube = cmds.polyCube(width=2, hight=5, depth=2)[0]
    return cube


# ===================================================================
# BUG 3: AttributeError
# "AttributeError: module 'maya.cmds' has no attribute 'polycube'"
# Cause: Wrong capitalization of a Maya command.  Maya commands are
#        camelCase: polyCube, polyPlane, shadingNode.
# Fix:   Change 'polycube' to 'polyCube'.
# ===================================================================
def bug_attribute_error():
    # Maya uses camelCase -- 'polycube' should be 'polyCube'
    cube = cmds.polycube(name="test_cube")[0]
    return cube


# ===================================================================
# BUG 4: IndexError
# "IndexError: list index out of range"
# Cause: Trying to access an index that doesn't exist.
#        A list with 3 items has indices 0, 1, 2 -- not 3.
# Fix:   Use index 2 for the last item, or use [-1].
# ===================================================================
def bug_index_error():
    colors = ["red", "green", "blue"]
    # There are only 3 items (indices 0, 1, 2).  Index 3 is out of range.
    favorite = colors[3]
    print("My favorite color is: " + favorite)


# ===================================================================
# BUG 5: KeyError
# "KeyError: 'colour'"
# Cause: Accessing a dictionary with a key that doesn't exist.
#        British spelling 'colour' vs American 'color'.
# Fix:   Use the exact key that was defined: 'color'.
# ===================================================================
def bug_key_error():
    settings = {
        "color": (1, 0, 0),
        "height": 5,
        "name": "tower",
    }
    # 'colour' is not a key in this dict -- should be 'color'
    rgb = settings["colour"]
    print("Color is:", rgb)


# ===================================================================
# BUG 6: ValueError
# "ValueError: could not convert string to float: 'five'"
# Cause: Trying to convert a word to a number.  Python can convert
#        "5" (a digit string) but not "five" (a word).
# Fix:   Use the numeric string "5" or the integer 5.
# ===================================================================
def bug_value_error():
    user_input = "five"
    height = float(user_input)
    print("Building height:", height)


# ===================================================================
# BUG 7: SyntaxError (BONUS -- can't even define the function)
# If you uncomment this, Python will refuse to load the ENTIRE file
# because it can't parse the broken syntax.
# Cause: Missing closing parenthesis.
# Fix:   Add the missing ')'.
# ===================================================================
# def bug_syntax_error():
#     cube = cmds.polyCube(
#         width=2,
#         height=5
#                           # <-- missing closing )
#     cmds.move(0, 3, 0, cube)


# ===================================================================
# RUNNER: Uncomment one call at a time to study each error.
# ===================================================================
def run_demo():
    """Uncomment ONE bug function call at a time, then run the script."""
    cmds.file(new=True, force=True)
    print("--- Demo: Reading Error Messages ---")
    print("Uncomment one bug call below, then re-run.\n")

    # bug_name_error()
    # bug_type_error()
    # bug_attribute_error()
    # bug_index_error()
    # bug_key_error()
    # bug_value_error()

    print("All bug functions are commented out.  Uncomment one to try it!")


run_demo()
