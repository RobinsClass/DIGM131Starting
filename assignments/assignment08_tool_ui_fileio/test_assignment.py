"""
Self-check tests for Assignment 8: Maya Tool with UI and File I/O.

Run this file from your assignment folder:
    python test_assignment.py

These tests analyze your code structure WITHOUT running it (no Maya needed).
They help you verify your work before submitting.
"""

import ast
import os
import re
import sys
import unittest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_and_parse(filename):
    """Read a Python file and return (source_text, ast_tree) or raise."""
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Could not find '{filename}' in {os.path.dirname(__file__)}")
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source, filename=filename)
    return source, tree


def _get_functions(tree):
    """Return all FunctionDef and AsyncFunctionDef nodes."""
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _has_docstring(node):
    """Return True if node has a docstring."""
    return (node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str))


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestAssignment08(unittest.TestCase):
    """Structural checks for Assignment 8 — Tool UI and File I/O."""

    @classmethod
    def setUpClass(cls):
        cls._files = {}
        cls._skip_reasons = {}
        for fname in ("tool_ui.py", "tool_logic.py"):
            try:
                source, tree = _read_and_parse(fname)
                cls._files[fname] = (source, tree)
            except FileNotFoundError as exc:
                cls._skip_reasons[fname] = str(exc)

    def _require(self, fname):
        if fname not in self._files:
            self.skipTest(self._skip_reasons.get(fname, f"{fname} not found"))
        return self._files[fname]

    # -- tests --

    def test_01_tool_ui_exists(self):
        """Check that tool_ui.py exists and is valid Python."""
        source, tree = self._require("tool_ui.py")
        self.assertIsNotNone(tree)

    def test_02_tool_logic_exists(self):
        """Check that tool_logic.py exists and is valid Python."""
        source, tree = self._require("tool_logic.py")
        self.assertIsNotNone(tree)

    def test_03_ui_contains_window(self):
        """Check that tool_ui.py creates a Maya window (cmds.window)."""
        source, tree = self._require("tool_ui.py")
        found = "cmds.window" in source or "mc.window" in source
        self.assertTrue(found,
                        "Could not find 'cmds.window' in tool_ui.py. "
                        "Your UI file should create a Maya window for the tool.")

    def test_04_ui_has_callback_functions(self):
        """Check that tool_ui.py has at least 3 callback functions."""
        source, tree = self._require("tool_ui.py")
        funcs = _get_functions(tree)
        # Callbacks are functions referenced by UI elements — we count all functions
        # as potential callbacks. At minimum 3 for a meaningful UI.
        self.assertGreaterEqual(len(funcs), 3,
                                f"Found {len(funcs)} function(s) in tool_ui.py. "
                                "A good UI has at least 3 callback functions — one per button or control.")

    def test_05_logic_no_ui_commands(self):
        """Check that tool_logic.py does NOT contain UI commands (separation of concerns)."""
        source, tree = self._require("tool_logic.py")
        has_window = "cmds.window" in source or "mc.window" in source
        has_button = "cmds.button" in source or "mc.button" in source
        violations = []
        if has_window:
            violations.append("cmds.window")
        if has_button:
            violations.append("cmds.button")
        self.assertEqual(len(violations), 0,
                         f"Found UI commands in tool_logic.py: {violations}. "
                         "Keep UI code in tool_ui.py and logic in tool_logic.py. "
                         "This separation makes your code easier to maintain and test!")

    def test_06_logic_imports_json(self):
        """Check that tool_logic.py imports the json module (for file I/O)."""
        source, tree = self._require("tool_logic.py")
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "json":
                        found = True
            elif isinstance(node, ast.ImportFrom) and node.module == "json":
                found = True
        self.assertTrue(found,
                        "tool_logic.py should 'import json' for reading/writing data files. "
                        "JSON is the standard way to save and load structured data.")

    def test_07_has_save_and_load_functions(self):
        """Check for functions with 'save' and 'load' in their names."""
        source, tree = self._require("tool_logic.py")
        funcs = _get_functions(tree)
        names = [f.name.lower() for f in funcs]
        has_save = any("save" in n for n in names)
        has_load = any("load" in n for n in names)
        missing = []
        if not has_save:
            missing.append("save")
        if not has_load:
            missing.append("load")
        self.assertEqual(len(missing), 0,
                         f"Could not find function(s) for: {missing}. "
                         "Name your functions descriptively, e.g. 'save_settings' and 'load_settings'.")

    def test_08_ui_imports_tool_logic(self):
        """Check that tool_ui.py imports from tool_logic."""
        source, tree = self._require("tool_ui.py")
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and "tool_logic" in node.module:
                found = True
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if "tool_logic" in alias.name:
                        found = True
        self.assertTrue(found,
                        "tool_ui.py should import from tool_logic. "
                        "Example: 'from tool_logic import save_settings, load_settings'")

    def test_09_all_functions_have_docstrings(self):
        """Check that all functions in both files have docstrings."""
        missing = []
        for fname in ("tool_ui.py", "tool_logic.py"):
            if fname not in self._files:
                continue
            source, tree = self._files[fname]
            for fn in _get_functions(tree):
                if not _has_docstring(fn):
                    missing.append(f"{fname}: {fn.name}")
        self.assertEqual(len(missing), 0,
                         f"These functions are missing docstrings: {missing}. "
                         "Add a brief description as a triple-quoted string on the first line of each function.")

    def test_10_has_try_except(self):
        """Check for try/except blocks (error handling for file I/O)."""
        found = False
        for fname in ("tool_ui.py", "tool_logic.py"):
            if fname not in self._files:
                continue
            tree = self._files[fname][1]
            tries = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
            if tries:
                found = True
                break
        self.assertTrue(found,
                        "Neither file contains try/except blocks. "
                        "File I/O can fail (file not found, permission denied, bad JSON) — "
                        "wrap those operations in try/except!")

    def test_11_uses_context_manager_for_files(self):
        """Check for 'with' statements (context managers) for file I/O."""
        found = False
        for fname in ("tool_ui.py", "tool_logic.py"):
            if fname not in self._files:
                continue
            tree = self._files[fname][1]
            withs = [n for n in ast.walk(tree) if isinstance(n, ast.With)]
            if withs:
                found = True
                break
        self.assertTrue(found,
                        "Could not find any 'with' statements. "
                        "Always use 'with open(filepath) as f:' instead of plain 'open()'. "
                        "The 'with' statement ensures files are properly closed, even if errors occur.")


# ---------------------------------------------------------------------------
# Runner with friendly summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Assignment 8 Self-Check: Tool UI and File I/O")
    print("=" * 60)
    print()
    print("  These tests check your code STRUCTURE — they do NOT")
    print("  run your Maya commands. Use them to catch common")
    print("  issues before you submit.")
    print()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment08)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("-" * 60)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total = result.testsRun - len(result.skipped)
    if total == 0:
        print("  No tests could run. Make sure tool_ui.py and")
        print("  tool_logic.py exist in the same folder as this test file.")
    elif passed == total:
        print(f"  Fantastic! All {passed}/{total} checks passed!")
        print("  Your tool architecture looks clean. Well done!")
    else:
        print(f"  {passed}/{total} checks passed.")
        print("  Review the messages above for guidance.")
        print("  Separating UI from logic is a real-world skill — worth getting right!")
    print("-" * 60)
