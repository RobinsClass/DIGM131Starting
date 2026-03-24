"""
Assignment 10: Final Project
DIGM 131 - Intro to Scripting for Digital Media

OBJECTIVE:
    Build a complete Maya tool that demonstrates the skills you have learned
    throughout the course. Your tool should be useful, polished, and well-
    documented.

============================================================================
REQUIREMENTS
============================================================================

FUNCTIONALITY (40%):
    - The tool must perform a meaningful task in Maya
    - It must use at least 5 different Maya commands
    - It must accept user input (UI or function parameters)
    - It must produce visible results in the viewport

CODE QUALITY (25%):
    - Organized into multiple functions (no single giant function)
    - All functions have docstrings with Args and Returns
    - Descriptive variable and function names (snake_case)
    - PEP 8 compliant (consistent indentation, spacing, line length)
    - No code duplication (use loops and helper functions)

ERROR HANDLING (15%):
    - All Maya commands wrapped in try/except
    - Input validation for all user-facing functions
    - Helpful error messages (what went wrong + how to fix)
    - The tool never crashes Maya

ARCHITECTURE (10%):
    - Logic separated from UI (if UI is included)
    - Code split across modules if appropriate
    - Constants and configuration at the top of files
    - Clear imports

DOCUMENTATION AND REFLECTION (10%):
    - README_template.txt completed
    - reflection_template.txt completed
    - Inline comments for complex logic

============================================================================
DELIVERABLES
============================================================================

    1. This file (main.py) - entry point for your tool
    2. Additional module files as needed (e.g., logic.py, ui.py, utils.py)
    3. README_template.txt - completed project documentation
    4. reflection_template.txt - completed personal reflection

============================================================================
PROJECT IDEAS (choose one or propose your own)
============================================================================

    - City Generator: procedurally build a city block with buildings, roads, trees
    - Character Poser: tool to pose a simple character rig with presets
    - Material Library: create, save, load, and apply material presets
    - Animation Tool: keyframe helper, motion path builder, or walk cycle tool
    - Modeling Assistant: operations like array, scatter, snap-to-grid
    - Scene Organizer: rename, group, color-code, and arrange objects
    - Asset Placer: place objects along curves, grids, or random distributions

============================================================================
"""

import maya.cmds as cmds

# TODO: Import your additional modules here
# import tool_logic
# import tool_ui


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TOOL_NAME = "My Final Project"
VERSION = "1.0"


# ---------------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------------
def main():
    """Entry point for the final project tool.

    TODO: Set up and launch your tool here. This might include:
        - Clearing previous UI windows
        - Initializing any data structures
        - Creating the UI (if applicable)
        - Or running the tool directly (if no UI)
    """
    print("{} v{}".format(TOOL_NAME, VERSION))

    # TODO: Launch your tool
    #   Example with UI:
    #       tool_ui.create_ui()
    #
    #   Example without UI:
    #       tool_logic.generate_scene(parameters)

    pass


if __name__ == "__main__":
    main()
