"""
DIGM 131 - Assignment 2: Procedural Pattern Generator
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


STUDENT_FILE = "pattern_generator.py"


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


def _find_nested_for(node):
    """Recursively check if any ast.For node contains another ast.For."""
    if isinstance(node, ast.For):
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.For):
                return True
    return False


def _find_if_inside_loop(node):
    """Check if an ast.If exists inside any loop body."""
    for loop_node in ast.walk(node):
        if not isinstance(loop_node, (ast.For, ast.While)):
            continue
        for child in ast.walk(loop_node):
            if child is loop_node:
                continue
            if isinstance(child, ast.If):
                return True
    return False


class TestAssignment02(unittest.TestCase):
    """Tests for Assignment 2 - Procedural Pattern Generator."""

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
        """Check that pattern_generator.py exists and has no syntax errors."""
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

    def test_has_nested_for_loop(self):
        """Check that you have at least one nested for-loop (a for-loop inside another for-loop)."""
        tree = self._require_tree()
        found = False
        for node in ast.walk(tree):
            if _find_nested_for(node):
                found = True
                break
        self.assertTrue(
            found,
            "No nested for-loop found. A pattern generator typically needs\n"
            "  a loop inside a loop -- for example, one loop for rows and\n"
            "  another for columns:\n"
            "    for row in range(5):\n"
            "        for col in range(5):\n"
            "            ..."
        )

    def test_has_conditional_inside_loop(self):
        """Check that you have at least one if-statement inside a loop (to vary the pattern)."""
        tree = self._require_tree()
        found = _find_if_inside_loop(tree)
        self.assertTrue(
            found,
            "No if-statement found inside a loop. Patterns usually need\n"
            "  conditionals to decide what to create at each position.\n"
            "  For example:\n"
            "    for i in range(10):\n"
            "        if i % 2 == 0:\n"
            "            # create one type of object\n"
            "        else:\n"
            "            # create another type"
        )

    def test_uses_range(self):
        """Check that you use range() to control your loops."""
        tree = self._require_tree()
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id == "range":
                    found = True
                    break
        self.assertTrue(
            found,
            "No call to range() found. Use range() to control how many\n"
            "  times your loops run. For example: for i in range(10):"
        )

    def test_has_at_least_five_comment_lines(self):
        """Check that you have at least 5 lines with comments (# ...) to explain your code."""
        source = self._require_source()
        lines = source.split("\n")
        comment_lines = []
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Count lines that have a comment (inline or standalone)
            if "#" in stripped and not stripped.startswith('"""') and not stripped.startswith("'''"):
                # Make sure # is not inside a string (rough heuristic)
                code_before = stripped.split("#")[0]
                # If quote count is even, the # is likely a real comment
                if code_before.count('"') % 2 == 0 and code_before.count("'") % 2 == 0:
                    comment_lines.append(i)

        self.assertGreaterEqual(
            len(comment_lines), 5,
            f"Found only {len(comment_lines)} line(s) with comments.\n"
            f"  Add comments to explain your logic -- at least 5 comment lines.\n"
            f"  Good comments explain WHY, not just WHAT."
        )

    def test_if_statements_have_nearby_comments(self):
        """Check that each if-statement has a comment on the same line or within 2 lines above it."""
        source = self._require_source()
        tree = self._require_tree()
        lines = source.split("\n")

        if_lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if_lines.append(node.lineno)

        if not if_lines:
            self.skipTest("No if-statements found to check.")

        uncommented_ifs = []
        for if_line in if_lines:
            # Check lines: same line, 1 above, 2 above
            has_comment = False
            for offset in range(0, 3):
                check_line = if_line - offset
                if 1 <= check_line <= len(lines):
                    line_text = lines[check_line - 1]
                    if "#" in line_text:
                        has_comment = True
                        break
            if not has_comment:
                uncommented_ifs.append(if_line)

        self.assertEqual(
            len(uncommented_ifs), 0,
            f"The if-statement(s) on line(s) {uncommented_ifs} don't have a comment\n"
            f"  on the same line or within 2 lines above. Add a brief comment\n"
            f"  explaining the condition. For example:\n"
            f"    # Alternate between cubes and spheres\n"
            f"    if i % 2 == 0:"
        )

    def test_comments_are_meaningful(self):
        """Check that at least 3 comments go beyond just restating the code."""
        source = self._require_source()
        lines = source.split("\n")

        # Patterns that suggest a comment just restates the code
        trivial_patterns = [
            r"^#\s*(set|create|assign|define|declare|make)\s+(a\s+)?variable",
            r"^#\s*(set|assign)\s+\w+\s*(to|=)",
            r"^#\s*import",
            r"^#\s*loop",
            r"^#\s*end\s*(of)?\s*(loop|if|else|function)",
            r"^#\s*else",
            r"^#\s*if\s+\w+",
            r"^#\s*increment",
            r"^#\s*print",
        ]

        meaningful_count = 0
        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            # Skip shebang and encoding lines
            if stripped.startswith("#!") or "coding" in stripped:
                continue
            comment_text = stripped
            is_trivial = False
            for pattern in trivial_patterns:
                if re.match(pattern, comment_text, re.IGNORECASE):
                    is_trivial = True
                    break
            if not is_trivial and len(comment_text) > 3:
                meaningful_count += 1

        self.assertGreaterEqual(
            meaningful_count, 3,
            f"Found only {meaningful_count} meaningful comment(s).\n"
            f"  Good comments explain WHY you're doing something, not just WHAT.\n"
            f"  Instead of: '# set x to 5'\n"
            f"  Try:        '# spacing between each column of objects'"
        )

    def test_has_enough_code(self):
        """Check that the file has a reasonable amount of code for a pattern generator."""
        source = self._require_source()
        lines = source.split("\n")
        code_lines = [
            l for l in lines
            if l.strip() and not l.strip().startswith("#")
        ]
        self.assertGreaterEqual(
            len(code_lines), 12,
            f"Your file has only {len(code_lines)} lines of code.\n"
            f"  A pattern generator with nested loops and conditionals should\n"
            f"  have more code. Keep building your pattern!"
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
            self.stream.write("  Fantastic! All checks passed!\n")
        elif self.successes >= self.total - 2:
            self.stream.write("  So close! Just a couple things to polish.\n")
        else:
            self.stream.write("  Keep at it -- you're making progress!\n")
        self.stream.write("=" * 60 + "\n")


class FriendlyRunner(unittest.TextTestRunner):
    """Test runner that uses the friendly summary."""

    def run(self, test):
        result = FriendlySummary(sys.stdout, True, self.verbosity)
        sys.stdout.write("\n" + "=" * 60 + "\n")
        sys.stdout.write("  Assignment 2: Procedural Pattern Generator - Self-Check\n")
        sys.stdout.write("=" * 60 + "\n\n")
        test(result)
        result.printSummary()
        return result


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment02)
    runner = FriendlyRunner()
    runner.run(suite)
