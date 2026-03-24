"""
DIGM 131 - Assignment 4: Data-Driven Scene Generator
Self-Check Unit Tests

Run this file from your assignment folder:
    python test_assignment.py

These tests check your code's STRUCTURE without running it (no Maya needed).
They help you catch common issues before submitting. Good luck!
"""

import ast
import os
import re
import sys
import unittest


STUDENT_FILE = "data_driven_scene.py"


def get_file_path():
    """Return the absolute path to the student file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), STUDENT_FILE)


def read_source():
    """Read the student file as plain text."""
    path = get_file_path()
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_ast():
    """Parse the student file into an AST tree."""
    source = read_source()
    if source is None:
        return None
    try:
        return ast.parse(source)
    except SyntaxError:
        return None


def get_function_defs(tree):
    """Return all FunctionDef nodes."""
    if tree is None:
        return []
    return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_docstring(func_node):
    """Extract the docstring from a function node, or return None."""
    if (func_node.body
            and isinstance(func_node.body[0], ast.Expr)
            and isinstance(func_node.body[0].value, (ast.Constant, ast.Str))):
        val = func_node.body[0].value
        if isinstance(val, ast.Constant):
            return val.value if isinstance(val.value, str) else None
        return val.s
    return None


def find_list_of_dicts(tree):
    """Find ast.List nodes that contain ast.Dict elements. Return a list of (list_node, dict_count)."""
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.List) and node.elts:
            dict_count = sum(1 for el in node.elts if isinstance(el, ast.Dict))
            if dict_count > 0:
                results.append((node, dict_count))
    return results


def get_string_constants_in_dicts(tree):
    """Collect string constant values used as dict values across all dicts in lists."""
    type_values = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.List):
            for el in node.elts:
                if isinstance(el, ast.Dict):
                    for key, val in zip(el.keys, el.values):
                        # Look for keys named "type" or similar
                        key_name = None
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            key_name = key.value
                        elif isinstance(key, ast.Str):
                            key_name = key.s
                        if key_name and key_name.lower() in ("type", "shape", "object_type", "obj_type", "kind"):
                            if isinstance(val, ast.Constant) and isinstance(val.value, str):
                                type_values.add(val.value)
                            elif isinstance(val, ast.Str):
                                type_values.add(val.s)
    return type_values


class TestAssignment04(unittest.TestCase):
    """Tests for Assignment 4 - Data-Driven Scene Generator."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _require_source(self):
        source = read_source()
        self.assertIsNotNone(
            source,
            f"Could not find '{STUDENT_FILE}'. Make sure the file exists "
            f"in the same folder as this test."
        )
        return source

    def _require_tree(self):
        tree = parse_ast()
        self.assertIsNotNone(
            tree,
            f"'{STUDENT_FILE}' has a SyntaxError and cannot be parsed. "
            f"Open it in your editor and fix any red underlines first!"
        )
        return tree

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------
    def test_file_exists_and_parses(self):
        """Check that data_driven_scene.py exists and has no syntax errors."""
        path = get_file_path()
        self.assertTrue(
            os.path.exists(path),
            f"'{STUDENT_FILE}' not found. Did you name it correctly?"
        )
        source = read_source()
        try:
            ast.parse(source)
        except SyntaxError as e:
            self.fail(
                f"'{STUDENT_FILE}' has a SyntaxError on line {e.lineno}: {e.msg}\n"
                f"  Fix this before running the tests again."
            )

    def test_has_list_of_dictionaries(self):
        """Check that the file contains a list of dictionaries (the scene data)."""
        tree = self._require_tree()
        lod = find_list_of_dicts(tree)
        self.assertTrue(
            len(lod) > 0,
            "No list of dictionaries found. Your scene data should look like:\n"
            '  scene_data = [\n'
            '      {"type": "cube", "position": [0, 0, 0], "scale": [1, 1, 1]},\n'
            '      {"type": "sphere", "position": [3, 0, 0], "scale": [2, 2, 2]},\n'
            '      ...\n'
            '  ]'
        )

    def test_list_has_at_least_ten_entries(self):
        """Check that your data list has at least 10 dictionary entries (10+ objects in your scene)."""
        tree = self._require_tree()
        lod = find_list_of_dicts(tree)
        if not lod:
            self.skipTest("No list of dictionaries found.")

        max_count = max(count for _, count in lod)
        self.assertGreaterEqual(
            max_count, 10,
            f"Your largest list of dictionaries has only {max_count} entries.\n"
            f"  A data-driven scene should define at least 10 objects in the data.\n"
            f"  Add more entries to create a richer scene!"
        )

    def test_data_has_variety(self):
        """Check that your data uses at least 3 different object types (variety in the scene)."""
        tree = self._require_tree()
        type_values = get_string_constants_in_dicts(tree)
        self.assertGreaterEqual(
            len(type_values), 3,
            f"Found only {len(type_values)} different type value(s): {type_values}\n"
            f"  Use at least 3 different types in your data (e.g., 'cube',\n"
            f"  'sphere', 'cylinder'). Make sure your dict key is named\n"
            f"  'type', 'shape', 'object_type', or 'kind'."
        )

    def test_has_functions_with_defaults(self):
        """Check that at least one function has default parameter values."""
        tree = self._require_tree()
        funcs = get_function_defs(tree)
        has_defaults = any(
            f.args.defaults or f.args.kw_defaults
            for f in funcs
        )
        self.assertTrue(
            has_defaults,
            "No function with default parameter values found.\n"
            "  Use defaults to make your functions more flexible:\n"
            '    def create_object(obj_type="cube", scale=1.0):\n'
            '        ...'
        )

    def test_function_names_are_snake_case(self):
        """Check that all function names follow snake_case convention."""
        tree = self._require_tree()
        funcs = get_function_defs(tree)
        snake_case = re.compile(r"^[a-z_][a-z0-9_]*$")
        bad = [f.name for f in funcs if not snake_case.match(f.name)]
        self.assertEqual(
            len(bad), 0,
            f"These function names are not snake_case: {bad}\n"
            f"  Python convention: 'createObject' -> 'create_object'"
        )

    def test_uses_four_space_indentation(self):
        """Check PEP 8: code uses 4-space indentation (no tabs, indentation is a multiple of 4)."""
        source = self._require_source()
        lines = source.split("\n")
        tab_lines = []
        bad_indent_lines = []

        for i, line in enumerate(lines, start=1):
            if "\t" in line:
                tab_lines.append(i)
            if line and not line.strip() == "":
                leading = len(line) - len(line.lstrip(" \t"))
                # Only check lines that are indented and don't start with tab
                if leading > 0 and "\t" not in line[:leading]:
                    if leading % 4 != 0:
                        bad_indent_lines.append(i)

        if tab_lines:
            self.fail(
                f"Found tab characters on line(s): {tab_lines[:5]}\n"
                f"  Python style (PEP 8) requires 4 spaces for indentation.\n"
                f"  Configure your editor to use spaces instead of tabs."
            )
        # Allow a few off lines (could be continuation lines)
        self.assertLessEqual(
            len(bad_indent_lines), 3,
            f"Lines with non-standard indentation (not a multiple of 4 spaces):\n"
            f"  {bad_indent_lines[:10]}\n"
            f"  PEP 8 recommends 4 spaces per indent level."
        )

    def test_all_functions_have_docstrings(self):
        """Check that every function has a docstring explaining what it does."""
        tree = self._require_tree()
        funcs = get_function_defs(tree)
        missing = [f.name for f in funcs if get_docstring(f) is None]
        self.assertEqual(
            len(missing), 0,
            f"These functions are missing docstrings: {missing}\n"
            f"  Add a docstring right after the def line:\n"
            f'    def create_object(data):\n'
            f'        """Create a Maya object from the given data dictionary."""'
        )

    def test_has_loop_over_data(self):
        """Check that there is at least one for-loop that iterates over data to create objects."""
        tree = self._require_tree()
        for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
        self.assertGreaterEqual(
            len(for_nodes), 1,
            "No for-loop found. A data-driven scene should loop over\n"
            "  your list of dictionaries to create each object:\n"
            "    for item in scene_data:\n"
            "        create_object(item)"
        )

    def test_has_enough_functions(self):
        """Check that the file defines at least 2 functions (to process data and create objects)."""
        tree = self._require_tree()
        funcs = get_function_defs(tree)
        self.assertGreaterEqual(
            len(funcs), 2,
            f"Found only {len(funcs)} function(s). You should have at least 2:\n"
            f"  one to process/create objects, and another to set up or\n"
            f"  orchestrate the scene."
        )


# ======================================================================
# Friendly summary
# ======================================================================
class FriendlySummary(unittest.TestResult):
    """Custom test result that prints a friendly summary at the end."""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.successes = 0
        self.total = 0

    def startTest(self, test):
        super().startTest(test)
        self.total += 1

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes += 1
        self.stream.write(f"  PASS: {test.shortDescription()}\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"  FAIL: {test.shortDescription()}\n")
        msg = str(err[1])
        for line in msg.split("\n"):
            self.stream.write(f"        {line}\n")
        self.stream.write("\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"  ERROR: {test.shortDescription()}\n")
        self.stream.write(f"        {err[1]}\n\n")

    def printSummary(self):
        self.stream.write("\n" + "=" * 60 + "\n")
        self.stream.write(f"  Score: {self.successes}/{self.total} checks passed\n")
        if self.successes == self.total:
            self.stream.write("  Great job! All checks passed!\n")
        elif self.successes >= self.total - 2:
            self.stream.write("  Almost perfect! A couple things to address.\n")
        else:
            self.stream.write("  Keep refining -- data-driven design is powerful!\n")
        self.stream.write("=" * 60 + "\n")


class FriendlyRunner(unittest.TextTestRunner):
    """Test runner that uses the friendly summary."""

    def run(self, test):
        result = FriendlySummary(sys.stdout, True, self.verbosity)
        sys.stdout.write("\n" + "=" * 60 + "\n")
        sys.stdout.write("  Assignment 4: Data-Driven Scene Generator - Self-Check\n")
        sys.stdout.write("=" * 60 + "\n\n")
        test(result)
        result.printSummary()
        return result


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment04)
    runner = FriendlyRunner()
    runner.run(suite)
