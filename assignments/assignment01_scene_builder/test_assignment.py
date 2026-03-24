"""
DIGM 131 - Assignment 1: Procedural Scene Builder
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


STUDENT_FILE = "scene_builder.py"


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


class TestAssignment01(unittest.TestCase):
    """Tests for Assignment 1 - Procedural Scene Builder."""

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
        """Check that scene_builder.py exists and has no syntax errors."""
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

    def test_imports_maya_cmds(self):
        """Check that the file imports maya.cmds (required for Maya scenes)."""
        source = self._require_source()
        has_import = bool(
            re.search(r"import\s+maya\.cmds", source)
            or re.search(r"from\s+maya\.cmds\s+import", source)
            or re.search(r"from\s+maya\s+import\s+cmds", source)
        )
        self.assertTrue(
            has_import,
            "Your file should import maya.cmds. For example:\n"
            "  import maya.cmds as cmds"
        )

    def test_has_header_comment(self):
        """Check that the file starts with a comment or docstring (good practice!)."""
        source = self._require_source()
        lines = source.split("\n")
        first_meaningful = ""
        for line in lines:
            stripped = line.strip()
            if stripped:
                first_meaningful = stripped
                break
        starts_with_comment = first_meaningful.startswith("#")
        starts_with_docstring = first_meaningful.startswith('"""') or first_meaningful.startswith("'''")
        self.assertTrue(
            starts_with_comment or starts_with_docstring,
            "Start your file with a header comment or docstring describing\n"
            "  what the script does. Example:\n"
            '  # Assignment 1: My Procedural Scene\n'
            '  # Creates a desert landscape with cacti and rocks'
        )

    def test_creates_at_least_five_objects(self):
        """Check that at least 5 Maya objects are created (cmds.poly* or cmds.create calls)."""
        source = self._require_source()
        # Match calls like cmds.polyCube, cmds.polySphere, cmds.createNode, etc.
        poly_calls = re.findall(
            r"cmds\.\s*(poly\w+|create\w*|sphere|circle|curve|joint|spaceLocator|group|instance|duplicate)",
            source,
            re.IGNORECASE,
        )
        count = len(poly_calls)
        self.assertGreaterEqual(
            count, 5,
            f"Found only {count} object-creation call(s) (cmds.poly*, cmds.create*, etc.).\n"
            f"  Your scene should create at least 5 objects. Keep building!"
        )

    def test_descriptive_variable_names(self):
        """Check that you use descriptive variable names (length > 3) for at least 8 assignments."""
        tree = self._require_tree()
        # Allowed short names
        allowed_short = {"i", "j", "k", "x", "y", "z", "_"}
        descriptive_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.startswith("_"):
                            continue
                        if len(name) > 3:
                            descriptive_count += 1

        self.assertGreaterEqual(
            descriptive_count, 8,
            f"Found only {descriptive_count} variable assignment(s) with descriptive names "
            f"(more than 3 characters).\n"
            f"  Use names like 'cube_height' or 'tree_position' instead of 'h' or 'pos'.\n"
            f"  Aim for at least 8 descriptive variable names."
        )

    def test_no_single_letter_variables(self):
        """Check that you avoid single-letter variable names (except i/j/k for loops, x/y/z for coords)."""
        tree = self._require_tree()
        allowed_short = {"i", "j", "k", "x", "y", "z", "_"}
        bad_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if len(name) == 1 and name not in allowed_short:
                            bad_names.add(name)

        self.assertEqual(
            len(bad_names), 0,
            f"Found single-letter variable name(s): {sorted(bad_names)}\n"
            f"  Rename these to something descriptive. For example, use 'width'\n"
            f"  instead of 'w', or 'height' instead of 'h'.\n"
            f"  (Exception: i/j/k in loops and x/y/z for coordinates are fine.)"
        )

    def test_no_cryptic_short_names(self):
        """Check that variable names like a, b, h, w are not used (use descriptive names instead)."""
        tree = self._require_tree()
        cryptic = {"a", "b", "c", "d", "e", "f", "g", "h", "l", "m", "n",
                    "o", "p", "q", "r", "s", "t", "u", "v", "w"}
        found = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in cryptic:
                        found.add(target.id)

        self.assertEqual(
            len(found), 0,
            f"Found short/cryptic variable name(s): {sorted(found)}\n"
            f"  These are hard to understand later. Rename them:\n"
            f"    h -> height,  w -> width,  s -> scale,  r -> radius, etc."
        )

    def test_has_enough_code(self):
        """Check that the file has a reasonable amount of code (at least 15 non-blank, non-comment lines)."""
        source = self._require_source()
        lines = source.split("\n")
        code_lines = [
            l for l in lines
            if l.strip() and not l.strip().startswith("#")
        ]
        self.assertGreaterEqual(
            len(code_lines), 15,
            f"Your file has only {len(code_lines)} lines of code.\n"
            f"  A scene with 5+ objects should have more code. Keep going!"
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
        # Print the assertion message nicely
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
            self.stream.write("  Awesome work! All checks passed!\n")
        elif self.successes >= self.total - 2:
            self.stream.write("  Almost there! Just a few things to fix.\n")
        else:
            self.stream.write("  Keep working on it -- you've got this!\n")
        self.stream.write("=" * 60 + "\n")


class FriendlyRunner(unittest.TextTestRunner):
    """Test runner that uses the friendly summary."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, test):
        result = FriendlySummary(sys.stdout, True, self.verbosity)
        sys.stdout.write("\n" + "=" * 60 + "\n")
        sys.stdout.write("  Assignment 1: Procedural Scene Builder - Self-Check\n")
        sys.stdout.write("=" * 60 + "\n\n")
        test(result)
        result.printSummary()
        return result


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment01)
    runner = FriendlyRunner()
    runner.run(suite)
