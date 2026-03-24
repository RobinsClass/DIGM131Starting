"""
Self-check tests for Assignment 6: Robust Toolkit with Error Handling.

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
    """Return all FunctionDef and AsyncFunctionDef nodes in *tree*."""
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _get_try_blocks(tree):
    """Return all ast.Try nodes."""
    return [node for node in ast.walk(tree) if isinstance(node, ast.Try)]


def _get_assert_stmts(tree):
    """Return all ast.Assert nodes."""
    return [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]


def _has_bare_except(try_node):
    """Return True if a Try node has a bare except (no exception type)."""
    for handler in try_node.handlers:
        if handler.type is None:
            return True
    return False


def _handler_has_descriptive_body(handler):
    """Return True if an except handler body contains a string literal (message)
    rather than just 'pass'."""
    for node in ast.walk(handler):
        # A string constant in a raise, print, or logging call counts
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) > 0:
            return True
    # Check if body is just 'pass'
    if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
        return False
    # If there's a raise with no message that's still better than pass
    for node in ast.walk(handler):
        if isinstance(node, ast.Raise):
            return True
    return True  # Has some logic, give benefit of the doubt


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestAssignment06(unittest.TestCase):
    """Structural checks for Assignment 6 — Robust Toolkit."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.source, cls.tree = _read_and_parse("robust_toolkit.py")
        except FileNotFoundError as exc:
            cls.source = None
            cls.tree = None
            cls._skip_reason = str(exc)

    # -- helpers --
    def _require_parsed(self):
        if self.tree is None:
            self.skipTest(self._skip_reason)

    # -- tests --

    def test_01_file_exists_and_parses(self):
        """Check that robust_toolkit.py exists and is valid Python."""
        self._require_parsed()
        self.assertIsNotNone(self.tree,
                             "Great start! Your file exists and is valid Python.")

    def test_02_at_least_five_functions(self):
        """Check that you defined at least 5 functions."""
        self._require_parsed()
        funcs = _get_functions(self.tree)
        self.assertGreaterEqual(len(funcs), 5,
                                f"Found {len(funcs)} function(s) but the assignment asks for at least 5. "
                                "Keep going — you've got this!")

    def test_03_at_least_three_try_except(self):
        """Check for at least 3 try/except blocks (error handling practice)."""
        self._require_parsed()
        tries = _get_try_blocks(self.tree)
        self.assertGreaterEqual(len(tries), 3,
                                f"Found {len(tries)} try/except block(s). "
                                "The assignment expects at least 3 — wrap risky operations in try/except.")

    def test_04_no_bare_except(self):
        """Check that every except clause specifies an exception type."""
        self._require_parsed()
        tries = _get_try_blocks(self.tree)
        bare = [t.lineno for t in tries if _has_bare_except(t)]
        self.assertEqual(len(bare), 0,
                         f"Found bare 'except:' (no exception type) on line(s) {bare}. "
                         "Always specify the exception type, e.g. 'except ValueError:'. "
                         "This is an important best practice!")

    def test_05_at_least_three_asserts(self):
        """Check for at least 3 assert statements (input validation)."""
        self._require_parsed()
        asserts = _get_assert_stmts(self.tree)
        self.assertGreaterEqual(len(asserts), 3,
                                f"Found {len(asserts)} assert statement(s). "
                                "The assignment asks for at least 3. "
                                "Use asserts to validate assumptions about your inputs!")

    def test_06_debug_mode_variable(self):
        """Check for a DEBUG_MODE variable assignment."""
        self._require_parsed()
        found = False
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "DEBUG_MODE":
                        found = True
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id == "DEBUG_MODE":
                    found = True
        self.assertTrue(found,
                        "Could not find a 'DEBUG_MODE = ...' assignment. "
                        "Add a DEBUG_MODE variable so you can toggle debug output on/off.")

    def test_07_functions_have_docstrings(self):
        """Check that every function has a docstring."""
        self._require_parsed()
        funcs = _get_functions(self.tree)
        missing = []
        for fn in funcs:
            if not (fn.body and isinstance(fn.body[0], ast.Expr)
                    and isinstance(fn.body[0].value, ast.Constant)
                    and isinstance(fn.body[0].value.value, str)):
                missing.append(fn.name)
        self.assertEqual(len(missing), 0,
                         f"These functions are missing docstrings: {missing}. "
                         "A docstring is a string on the very first line of your function. "
                         "It helps others (and future you) understand what the function does!")

    def test_08_input_validation_patterns(self):
        """Check for input validation (isinstance, type checks, or if+raise)."""
        self._require_parsed()
        has_isinstance = "isinstance" in self.source
        has_raise_in_if = False
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                for child in ast.walk(node):
                    if isinstance(child, ast.Raise):
                        has_raise_in_if = True
                        break
        has_type_check = "type(" in self.source
        found_any = has_isinstance or has_raise_in_if or has_type_check
        self.assertTrue(found_any,
                        "Could not find input validation patterns (isinstance(), type(), or if ... raise). "
                        "Validating inputs at the start of a function prevents confusing errors later!")

    def test_09_descriptive_error_messages(self):
        """Check that except blocks have descriptive messages, not just 'pass'."""
        self._require_parsed()
        tries = _get_try_blocks(self.tree)
        empty_handlers = []
        for t in tries:
            for handler in t.handlers:
                if not _handler_has_descriptive_body(handler):
                    empty_handlers.append(t.lineno)
        self.assertEqual(len(empty_handlers), 0,
                         f"Found except block(s) that just use 'pass' (near line(s) {empty_handlers}). "
                         "Add a descriptive message — print, log, or re-raise with a helpful string.")

    def test_10_uses_obj_exists(self):
        """Check for at least one use of cmds.objExists (common Maya validation)."""
        self._require_parsed()
        found = "cmds.objExists" in self.source or "mc.objExists" in self.source
        self.assertTrue(found,
                        "Could not find 'cmds.objExists' (or 'mc.objExists') in your code. "
                        "This is an important Maya function for checking if an object exists "
                        "before operating on it. Try adding it to at least one function!")


# ---------------------------------------------------------------------------
# Runner with friendly summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Assignment 6 Self-Check: Robust Toolkit")
    print("=" * 60)
    print()
    print("  These tests check your code STRUCTURE — they do NOT")
    print("  run your Maya commands. Use them to catch common")
    print("  issues before you submit.")
    print()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment06)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("-" * 60)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total = result.testsRun - len(result.skipped)
    if total == 0:
        print("  No tests could run. Make sure robust_toolkit.py exists")
        print("  in the same folder as this test file.")
    elif passed == total:
        print(f"  Fantastic! All {passed}/{total} checks passed!")
        print("  Your code structure looks great. Nice work!")
    else:
        print(f"  {passed}/{total} checks passed.")
        print("  Review the messages above for tips on what to fix.")
        print("  You're making progress — keep it up!")
    print("-" * 60)
