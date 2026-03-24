"""
Self-check tests for Assignment 9: Exploration Project.

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


def _is_snake_case(name):
    """Return True if *name* looks like snake_case."""
    if name.startswith("_"):
        name = name.lstrip("_")
    return bool(re.match(r"^[a-z][a-z0-9_]*$", name)) if name else True


def _count_distinct_cmds(source):
    """Count distinct cmds.xxx or mc.xxx command names in source."""
    pattern = r"(?:cmds|mc)\.([a-zA-Z_]\w*)"
    matches = set(re.findall(pattern, source))
    # Filter out common non-command attributes
    noise = {"__", "warning", "error"}
    return matches - noise


def _file_exists(filename):
    """Check if a file exists relative to this test file's directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    return os.path.isfile(path)


def _file_has_content(filename, min_chars=50):
    """Check if a file exists and has meaningful content."""
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.isfile(path):
        return False
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read().strip()
    return len(content) >= min_chars


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestAssignment09(unittest.TestCase):
    """Structural checks for Assignment 9 — Exploration Project."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.source, cls.tree = _read_and_parse("exploration_project.py")
        except FileNotFoundError as exc:
            cls.source = None
            cls.tree = None
            cls._skip_reason = str(exc)

    def _require_parsed(self):
        if self.tree is None:
            self.skipTest(self._skip_reason)

    # -- tests --

    def test_01_file_exists_and_parses(self):
        """Check that exploration_project.py exists and is valid Python."""
        self._require_parsed()
        self.assertIsNotNone(self.tree)

    def test_02_uses_diverse_cmds(self):
        """Check for at least 5 different cmds.xxx commands (exploring the API)."""
        self._require_parsed()
        cmds_used = _count_distinct_cmds(self.source)
        self.assertGreaterEqual(len(cmds_used), 5,
                                f"Found {len(cmds_used)} distinct cmds command(s): {sorted(cmds_used)}. "
                                "The point of this assignment is exploration — try at least 5 different "
                                "Maya commands to show what you discovered!")

    def test_03_has_functions(self):
        """Check that code is organized into functions (not just loose code)."""
        self._require_parsed()
        funcs = _get_functions(self.tree)
        self.assertGreaterEqual(len(funcs), 1,
                                "Your code should be organized into functions, not just loose statements. "
                                "Even for exploration, wrapping code in functions makes it reusable!")

    def test_04_functions_have_docstrings(self):
        """Check that all functions have docstrings."""
        self._require_parsed()
        funcs = _get_functions(self.tree)
        missing = [fn.name for fn in funcs if not _has_docstring(fn)]
        self.assertEqual(len(missing), 0,
                         f"These functions need docstrings: {missing}. "
                         "Describe what each function does and what you learned from writing it.")

    def test_05_has_inline_comments(self):
        """Check for inline comments explaining discoveries."""
        self._require_parsed()
        lines = self.source.split("\n")
        comment_lines = [line for line in lines
                         if "#" in line and not line.strip().startswith("#!")]
        # Count lines with comments (both full-line and inline)
        self.assertGreaterEqual(len(comment_lines), 5,
                                f"Found {len(comment_lines)} comment line(s). "
                                "Add more comments explaining what you tried and what you discovered. "
                                "This assignment is about documenting your learning process!")

    def test_06_has_error_handling(self):
        """Check for try/except blocks (handling unexpected results)."""
        self._require_parsed()
        tries = [n for n in ast.walk(self.tree) if isinstance(n, ast.Try)]
        self.assertGreaterEqual(len(tries), 1,
                                "No try/except blocks found. "
                                "When exploring new commands, things can go wrong — "
                                "wrap risky experiments in try/except to handle errors gracefully.")

    def test_07_learning_log_exists(self):
        """Check that learning_log_template.txt exists and has content."""
        exists = _file_has_content("learning_log_template.txt", min_chars=50)
        self.assertTrue(exists,
                        "learning_log_template.txt is missing or too short. "
                        "Fill in the learning log to reflect on what you explored and discovered. "
                        "This is an important part of the assignment!")

    def test_08_peer_review_exists(self):
        """Check that peer_review_template.txt exists and has content."""
        exists = _file_has_content("peer_review_template.txt", min_chars=50)
        self.assertTrue(exists,
                        "peer_review_template.txt is missing or too short. "
                        "Complete the peer review template — reviewing others' work "
                        "helps you learn too!")

    def test_09_snake_case_functions(self):
        """Check that function names follow PEP 8 (snake_case)."""
        self._require_parsed()
        funcs = _get_functions(self.tree)
        bad = [fn.name for fn in funcs if not _is_snake_case(fn.name)]
        self.assertEqual(len(bad), 0,
                         f"These function names are not snake_case: {bad}. "
                         "PEP 8 says function names should be lowercase_with_underscores.")

    def test_10_consistent_indentation(self):
        """Check that indentation uses 4 spaces (PEP 8 standard)."""
        self._require_parsed()
        lines = self.source.split("\n")
        tab_lines = []
        for i, line in enumerate(lines, 1):
            if line.startswith("\t"):
                tab_lines.append(i)
        self.assertEqual(len(tab_lines), 0,
                         f"Found tab characters on line(s) {tab_lines[:5]}{'...' if len(tab_lines) > 5 else ''}. "
                         "PEP 8 recommends 4 spaces for indentation, not tabs. "
                         "Most editors can convert tabs to spaces automatically.")


# ---------------------------------------------------------------------------
# Runner with friendly summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Assignment 9 Self-Check: Exploration Project")
    print("=" * 60)
    print()
    print("  These tests check your code STRUCTURE — they do NOT")
    print("  run your Maya commands. Use them to catch common")
    print("  issues before you submit.")
    print()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment09)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("-" * 60)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total = result.testsRun - len(result.skipped)
    if total == 0:
        print("  No tests could run. Make sure exploration_project.py")
        print("  exists in the same folder as this test file.")
    elif passed == total:
        print(f"  Fantastic! All {passed}/{total} checks passed!")
        print("  Your exploration project is well-structured. Nice work!")
    else:
        print(f"  {passed}/{total} checks passed.")
        print("  Check the messages above for tips.")
        print("  This assignment is about curiosity — keep exploring!")
    print("-" * 60)
