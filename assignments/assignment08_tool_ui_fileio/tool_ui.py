"""
Assignment 8: Maya Tool with UI and File I/O
DIGM 131 - Intro to Scripting for Digital Media

UI MODULE - This file handles the Maya window and user interface only.
All actual scene operations are in tool_logic.py.

OBJECTIVE:
    Build a Maya tool with a graphical interface (window with buttons, sliders,
    text fields) that lets the user perform scene operations. The tool must also
    save and load settings using JSON files.

REQUIREMENTS:
    1. Create a Maya window with at least:
       - A text field for user input (e.g., object name)
       - A slider or int field for a numeric value (e.g., count or size)
       - At least 3 buttons that trigger different operations
       - A "Save Settings" and "Load Settings" button
    2. Separate UI code (this file) from logic code (tool_logic.py)
    3. Save and load tool settings to/from a JSON file
    4. Handle errors in callbacks so the UI never crashes Maya
    5. Complete the self_test_checklist.txt

CONCEPTS PRACTICED:
    - Maya UI commands (cmds.window, cmds.button, cmds.textField, etc.)
    - Callback functions
    - Separation of concerns (UI vs. logic)
    - JSON file I/O
    - Lambda functions for passing arguments to callbacks

DELIVERABLES:
    - This file (tool_ui.py) with UI code
    - tool_logic.py with logic code
    - self_test_checklist.txt completed

SELF-TEST CHECKLIST (also in self_test_checklist.txt):
    [ ] Does the window open without errors?
    [ ] Does each button do what it should?
    [ ] Does it handle empty text fields?
    [ ] Does it handle impossible slider values?
    [ ] Does Save Settings create a JSON file?
    [ ] Does Load Settings restore the saved values?
    [ ] Does it give user feedback (print or cmds.confirmDialog)?
    [ ] Does it clean up if something fails?

NOTES:
    - Always check if a window exists before creating it (prevents duplicates)
    - Use cmds.warning() or cmds.confirmDialog() for user feedback, not just print
    - Lambda is useful for passing arguments: command=lambda *args: my_func(arg)
"""

import maya.cmds as cmds
import tool_logic

# ---------------------------------------------------------------------------
# Window configuration
# ---------------------------------------------------------------------------
WINDOW_NAME = "myToolWindow"
WINDOW_TITLE = "My Scene Tool"
WINDOW_WIDTH = 350


def create_ui():
    """Create the main tool window.

    This function should:
        1. Check if the window already exists and delete it if so
        2. Create a new window with cmds.window()
        3. Build the layout with all UI elements
        4. Show the window

    Returns:
        str: The name of the created window.
    """
    # --- Delete existing window if it exists ---
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    # --- Create the window ---
    cmds.window(WINDOW_NAME, title=WINDOW_TITLE, widthHeight=(WINDOW_WIDTH, 300))

    # TODO: Create a column layout
    #   cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    # TODO: Add a section header
    #   cmds.text(label="My Scene Tool", font="boldLabelFont", height=30)
    #   cmds.separator(height=10)

    # TODO: Add a text field for object name input
    #   Store the field name in a variable so callbacks can read from it
    #   Example:
    #       cmds.text(label="Object Name:")
    #       name_field = cmds.textField(text="myObject")

    # TODO: Add an integer slider for a numeric value (e.g., count)
    #   Example:
    #       cmds.text(label="Count:")
    #       count_slider = cmds.intSliderGrp(field=True, minValue=1, maxValue=20, value=5)

    # TODO: Add buttons that call your callback functions
    #   Example:
    #       cmds.button(label="Create Objects",
    #                   command=lambda *args: on_create_clicked(name_field, count_slider))

    # TODO: Add Save Settings and Load Settings buttons
    #   cmds.separator(height=10)
    #   cmds.button(label="Save Settings",
    #               command=lambda *args: on_save_clicked(name_field, count_slider))
    #   cmds.button(label="Load Settings",
    #               command=lambda *args: on_load_clicked(name_field, count_slider))

    # --- Show the window ---
    cmds.showWindow(WINDOW_NAME)

    # TODO: Return the window name
    pass


# ---------------------------------------------------------------------------
# Callback functions
# Each callback reads values from the UI, then calls a function in tool_logic.
# ---------------------------------------------------------------------------

def on_create_clicked(name_field, count_slider):
    """Callback for the Create button.

    Reads values from the UI elements and calls tool_logic to create objects.

    Args:
        name_field (str): The Maya UI element name for the text field.
        count_slider (str): The Maya UI element name for the int slider.
    """
    # TODO: Read the current value from the text field
    #   name = cmds.textField(name_field, query=True, text=True)

    # TODO: Read the current value from the slider
    #   count = cmds.intSliderGrp(count_slider, query=True, value=True)

    # TODO: Validate the inputs (non-empty name, reasonable count)

    # TODO: Call the appropriate function in tool_logic
    #   Wrap in try/except so the UI does not crash

    pass


def on_delete_clicked(name_field):
    """Callback for the Delete button.

    Args:
        name_field (str): The Maya UI element name for the text field.
    """
    # TODO: Read the name from the text field
    # TODO: Call tool_logic to delete matching objects
    # TODO: Give user feedback about what was deleted

    pass


def on_randomize_clicked(name_field):
    """Callback for a Randomize button (or another operation of your choice).

    Args:
        name_field (str): The Maya UI element name for the text field.
    """
    # TODO: Read values from the UI
    # TODO: Call the appropriate tool_logic function
    # TODO: Give user feedback

    pass


def on_save_clicked(name_field, count_slider):
    """Callback for Save Settings button.

    Reads current UI values and saves them to a JSON file.

    Args:
        name_field (str): The Maya UI element name for the text field.
        count_slider (str): The Maya UI element name for the int slider.
    """
    # TODO: Read current values from all UI elements
    # TODO: Build a dictionary with those values
    #   settings = {"name": name, "count": count}
    # TODO: Call tool_logic.save_settings(settings) or similar
    # TODO: Give user feedback ("Settings saved!")

    pass


def on_load_clicked(name_field, count_slider):
    """Callback for Load Settings button.

    Loads settings from a JSON file and populates the UI.

    Args:
        name_field (str): The Maya UI element name for the text field.
        count_slider (str): The Maya UI element name for the int slider.
    """
    # TODO: Call tool_logic.load_settings() to get the saved dictionary
    # TODO: Update the UI elements with the loaded values
    #   cmds.textField(name_field, edit=True, text=settings["name"])
    #   cmds.intSliderGrp(count_slider, edit=True, value=settings["count"])
    # TODO: Give user feedback ("Settings loaded!")
    # TODO: Handle the case where no settings file exists yet

    pass


# ---------------------------------------------------------------------------
# Launch the tool
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    create_ui()
