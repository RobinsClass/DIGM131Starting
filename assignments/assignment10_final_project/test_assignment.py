"""
Self-check tests for Assignment 10: Final Project (Comprehensive Maya Tool).

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

_THIS_DIR = os.path.dirname(__file__)


def _find_py_files():
    """Return list of .py files in this directory (excluding test files)."""
    files = []
    for fname in os.listdir(_THIS_DIR):
        if fname.endswith(".py") and not fname.startswith("test_"):
            files.append(fname)
    return sorted(files)


def _read_and_parse(filename):
    """Read a Python file and return (source_text, ast_tree) or raise."""
    path = os.path.join(_THIS_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Could not find '{filename}' in {_THIS_DIR}")
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source, filename=filename)
    return source, tree


def _get_functions(tree):
    """Return all FunctionDef and AsyncFunctionDef nodes."""
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _get_classes(tree):
    """Return all ClassDef nodes."""
    return [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]


def _has_docstring(node):
    """Return True if node has a docstring."""
    return (node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str))


def _is_snake_case(name):
    if name.startswith("_"):
        name = name.lstrip("_")
    return bool(re.match(r"^[a-z][a-z0-9_]*$", name)) if name else True


def _is_pascal_case(name):
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))


def _count_lines(source):
    """Count non-empty lines."""
    return len([l for l in source.split("\n") if l.strip()])


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestAssignment10(unittest.TestCase):
    """Structural checks for Assignment 10 — Final Project."""

    @classmethod
    def setUpClass(cls):
        cls.py_files = _find_py_files()
        cls.parsed = {}  # fname -> (source, tree)
        for fname in cls.py_files:
            try:
                cls.parsed[fname] = _read_and_parse(fname)
            except (SyntaxError, FileNotFoundError):
                pass  # will be caught by tests

    # -- tests --

    def test_01_at_least_three_py_files(self):
        """Check that the project has at least 3 Python files."""
        self.assertGreaterEqual(len(self.py_files), 3,
                                f"Found {len(self.py_files)} .py file(s): {self.py_files}. "
                                "A comprehensive final project should be split across at least 3 files "
                                "(e.g. main.py, ui.py, logic.py).")

    def test_02_all_files_parse(self):
        """Check that all Python files are valid (no syntax errors)."""
        failed = [f for f in self.py_files if f not in self.parsed]
        self.assertEqual(len(failed), 0,
                         f"These files have syntax errors and could not be parsed: {failed}. "
                         "Fix any syntax issues before submitting.")

    def test_03_total_function_count(self):
        """Check for at least 8 functions across all files."""
        total = 0
        for fname, (source, tree) in self.parsed.items():
            total += len(_get_functions(tree))
        self.assertGreaterEqual(total, 8,
                                f"Found {total} function(s) total across all files. "
                                "A comprehensive project needs at least 8 functions. "
                                "Break your code into small, focused functions!")

    def test_04_has_class(self):
        """Check for at least one class definition (encouraged for final project)."""
        total_classes = 0
        for fname, (source, tree) in self.parsed.items():
            total_classes += len(_get_classes(tree))
        if total_classes == 0:
            print("\n  NOTE: No classes found. Classes are encouraged but not strictly")
            print("  required for the final project. Consider using OOP to organize")
            print("  your tool — it shows mastery of the concepts from Assignment 7.")
        # This is a soft check — we always pass but print a note
        self.assertGreaterEqual(total_classes, 0)  # always passes

    def test_05_all_functions_have_docstrings(self):
        """Check that every function has a docstring."""
        missing = []
        for fname, (source, tree) in self.parsed.items():
            for fn in _get_functions(tree):
                if not _has_docstring(fn):
                    missing.append(f"{fname}: {fn.name}")
        self.assertEqual(len(missing), 0,
                         f"These functions are missing docstrings: {missing}. "
                         "Every function in your final project should be documented.")

    def test_06_module_level_docstrings(self):
        """Check that all files have module-level docstrings."""
        missing = []
        for fname, (source, tree) in self.parsed.items():
            if not _has_docstring(tree):
                missing.append(fname)
        self.assertEqual(len(missing), 0,
                         f"These files are missing module-level docstrings: {missing}. "
                         "Add a triple-quoted string at the top of each file describing its purpose.")

    def test_07_pep8_naming(self):
        """Check PEP 8 naming: snake_case for functions, PascalCase for classes."""
        bad_funcs = []
        bad_classes = []
        for fname, (source, tree) in self.parsed.items():
            for fn in _get_functions(tree):
                # Skip dunder methods
                if fn.name.startswith("__") and fn.name.endswith("__"):
                    continue
                if not _is_snake_case(fn.name):
                    bad_funcs.append(f"{fname}: {fn.name}")
            for cls in _get_classes(tree):
                if not _is_pascal_case(cls.name):
                    bad_classes.append(f"{fname}: {cls.name}")
        issues = []
        if bad_funcs:
            issues.append(f"Non-snake_case functions: {bad_funcs}")
        if bad_classes:
            issues.append(f"Non-PascalCase classes: {bad_classes}")
        self.assertEqual(len(issues), 0,
                         " | ".join(issues) + " — "
                         "Follow PEP 8: function_names_like_this, ClassNamesLikeThis.")

    def test_08_has_error_handling(self):
        """Check for try/except blocks across the project."""
        total_tries = 0
        for fname, (source, tree) in self.parsed.items():
            total_tries += len([n for n in ast.walk(tree) if isinstance(n, ast.Try)])
        self.assertGreaterEqual(total_tries, 1,
                                "No try/except blocks found anywhere in the project. "
                                "A polished tool handles errors gracefully!")

    def test_09_has_input_validation(self):
        """Check for input validation patterns (isinstance, type checks, if+raise)."""
        found = False
        for fname, (source, tree) in self.parsed.items():
            if "isinstance" in source or "type(" in source:
                found = True
                break
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Raise):
                            found = True
                            break
                if found:
                    break
        self.assertTrue(found,
                        "No input validation found (isinstance, type(), or if+raise). "
                        "Validate inputs to make your tool robust!")

    def test_10_imports_json(self):
        """Check that at least one file imports json (file I/O requirement)."""
        found = False
        for fname, (source, tree) in self.parsed.items():
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "json":
                            found = True
                elif isinstance(node, ast.ImportFrom) and node.module == "json":
                    found = True
        self.assertTrue(found,
                        "No file imports 'json'. The final project requires file I/O — "
                        "use JSON to save/load settings or data.")

    def test_11_has_ui(self):
        """Check that at least one file contains cmds.window (UI requirement)."""
        found = False
        for fname, (source, tree) in self.parsed.items():
            if "cmds.window" in source or "mc.window" in source:
                found = True
                break
        self.assertTrue(found,
                        "No file contains 'cmds.window'. "
                        "The final project should have a Maya UI window.")

    def test_12_has_main_guard(self):
        """Check for 'if __name__ == \"__main__\":' in at least one file."""
        found = False
        for fname, (source, tree) in self.parsed.items():
            if 'if __name__' in source and '__main__' in source:
                found = True
                break
        self.assertTrue(found,
                        "No file has 'if __name__ == \"__main__\":'. "
                        "Add this guard to your main entry point so the script can be "
                        "both imported and run directly.")

    def test_13_no_file_exceeds_200_lines(self):
        """Check that no single file exceeds 200 lines (keep files focused)."""
        too_long = []
        for fname, (source, tree) in self.parsed.items():
            line_count = len(source.split("\n"))
            if line_count > 200:
                too_long.append(f"{fname} ({line_count} lines)")
        self.assertEqual(len(too_long), 0,
                         f"These files are over 200 lines: {too_long}. "
                         "Break large files into smaller modules — each file should have a clear purpose.")

    def test_14_readme_exists(self):
        """Check that a README file exists."""
        candidates = ["README_template.txt", "README.txt", "README.md", "readme.txt", "readme.md"]
        found = any(os.path.isfile(os.path.join(_THIS_DIR, c)) for c in candidates)
        self.assertTrue(found,
                        "No README file found. Create a README (rename README_template.txt if provided) "
                        "to describe your project, how to use it, and what you learned.")

    def test_15_comment_density(self):
        """Check for adequate comments (at least 1 comment per 10 lines of code)."""
        total_code_lines = 0
        total_comment_lines = 0
        for fname, (source, tree) in self.parsed.items():
            lines = source.split("\n")
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('"""') and not stripped.startswith("'''"):
                    total_code_lines += 1
                if "#" in stripped:
                    total_comment_lines += 1
        if total_code_lines == 0:
            self.skipTest("No code found to check comment density.")
        expected = total_code_lines // 10
        self.assertGreaterEqual(total_comment_lines, expected,
                                f"Found {total_comment_lines} comment(s) across {total_code_lines} lines of code. "
                                f"Aim for at least 1 comment per 10 lines ({expected} minimum). "
                                "Comments explain the 'why' behind your code — they're especially "
                                "important in a final project!")


# ---------------------------------------------------------------------------
# Runner with friendly summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Assignment 10 Self-Check: Final Project")
    print("=" * 60)
    print()
    print("  These tests check your code STRUCTURE — they do NOT")
    print("  run your Maya commands. Use them to catch common")
    print("  issues before you submit.")
    print()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment10)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("-" * 60)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total = result.testsRun - len(result.skipped)
    if total == 0:
        print("  No tests could run. Make sure you have .py files")
        print("  in the same folder as this test file.")
    elif passed == total:
        print(f"  Outstanding! All {passed}/{total} checks passed!")
        print("  Your final project structure looks professional.")
        print("  You should be proud of how far you've come!")
    else:
        print(f"  {passed}/{total} checks passed.")
        print("  Review the messages above and polish your project.")
        print("  This is your chance to show everything you've learned!")
    print("-" * 60)
