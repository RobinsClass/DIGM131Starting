"""
DIGM 131 - Assignment 5: Multi-Module Maya Toolkit
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


def get_assignment_dir():
    """Return the directory containing this test file."""
    return os.path.dirname(os.path.abspath(__file__))


def find_py_files():
    """Find all .py files in the assignment directory (excluding test files)."""
    directory = get_assignment_dir()
    py_files = []
    for fname in os.listdir(directory):
        if fname.endswith(".py") and not fname.startswith("test_"):
            py_files.append(fname)
    return sorted(py_files)


def read_source(filename):
    """Read a file as plain text."""
    path = os.path.join(get_assignment_dir(), filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_file_ast(filename):
    """Parse a file into an AST tree."""
    source = read_source(filename)
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


def get_docstring_from_node(node):
    """Extract docstring from a function or module node, or return None."""
    if (node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
        val = node.body[0].value
        if isinstance(val, ast.Constant):
            return val.value if isinstance(val.value, str) else None
        return val.s
    return None


def get_module_docstring(tree):
    """Extract the module-level docstring."""
    return get_docstring_from_node(tree)


def count_lines(filename):
    """Count the number of lines in a file."""
    source = read_source(filename)
    if source is None:
        return 0
    return len(source.split("\n"))


def get_imports_from_file(tree):
    """Return a list of module names imported by the given AST."""
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


class TestAssignment05(unittest.TestCase):
    """Tests for Assignment 5 - Multi-Module Maya Toolkit."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_py_files(self):
        files = find_py_files()
        self.assertGreaterEqual(
            len(files), 3,
            f"Found only {len(files)} .py file(s): {files}\n"
            f"  A multi-module toolkit needs at least 3 Python files.\n"
            f"  For example: main.py, shapes.py, materials.py"
        )
        return files

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------
    def test_at_least_three_py_files(self):
        """Check that at least 3 .py files exist in the assignment directory."""
        files = find_py_files()
        self.assertGreaterEqual(
            len(files), 3,
            f"Found only {len(files)} .py file(s): {files}\n"
            f"  A multi-module toolkit needs at least 3 Python files.\n"
            f"  For example: main.py, shapes.py, transforms.py"
        )

    def test_each_file_has_module_docstring(self):
        """Check that every .py file starts with a module-level docstring."""
        files = self._get_py_files()
        missing = []
        for fname in files:
            tree = parse_file_ast(fname)
            if tree is None:
                missing.append(f"{fname} (could not parse)")
                continue
            doc = get_module_docstring(tree)
            if not doc:
                missing.append(fname)

        self.assertEqual(
            len(missing), 0,
            f"These files are missing a module-level docstring: {missing}\n"
            f"  Start each file with a docstring describing its purpose:\n"
            f'    """Utility functions for creating and placing trees."""'
        )

    def test_main_imports_from_other_modules(self):
        """Check that main.py imports from at least 2 other modules in the project."""
        files = find_py_files()
        # Find main.py (or similar entry point)
        main_file = None
        for candidate in ["main.py", "main_scene.py", "run.py", "toolkit.py"]:
            if candidate in files:
                main_file = candidate
                break
        if main_file is None:
            # Try to find any file that imports from 2+ local modules
            for fname in files:
                tree = parse_file_ast(fname)
                if tree is None:
                    continue
                imports = get_imports_from_file(tree)
                local_modules = [
                    os.path.splitext(f)[0] for f in files if f != fname
                ]
                local_imports = [imp for imp in imports if imp in local_modules]
                if len(local_imports) >= 2:
                    main_file = fname
                    break

        self.assertIsNotNone(
            main_file,
            "Could not find a main entry point file (main.py) or any file\n"
            "  that imports from at least 2 other project modules.\n"
            "  Create a main.py that ties your modules together."
        )

        tree = parse_file_ast(main_file)
        self.assertIsNotNone(tree, f"'{main_file}' has a SyntaxError.")

        imports = get_imports_from_file(tree)
        local_modules = [os.path.splitext(f)[0] for f in files if f != main_file]
        local_imports = [imp for imp in imports if imp in local_modules]

        self.assertGreaterEqual(
            len(local_imports), 2,
            f"'{main_file}' only imports from {len(local_imports)} local module(s): {local_imports}\n"
            f"  It should import from at least 2 of your other files:\n"
            f"  Available modules: {local_modules}"
        )

    def test_has_name_main_guard(self):
        """Check that at least one file has an if __name__ == '__main__': guard."""
        files = self._get_py_files()
        found = False
        for fname in files:
            source = read_source(fname)
            if source and re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', source):
                found = True
                break

        self.assertTrue(
            found,
            'No file has an if __name__ == "__main__": guard.\n'
            "  At least one file (usually main.py) should have this:\n"
            '    if __name__ == "__main__":\n'
            "        # code that runs when this file is executed directly"
        )

    def test_total_function_count(self):
        """Check that the total number of functions across all files is at least 8."""
        files = self._get_py_files()
        total = 0
        for fname in files:
            tree = parse_file_ast(fname)
            if tree:
                total += len(get_function_defs(tree))

        self.assertGreaterEqual(
            total, 8,
            f"Found only {total} function(s) across all files.\n"
            f"  A toolkit with 3+ modules should have at least 8 functions total.\n"
            f"  Break your code into small, reusable functions."
        )

    def test_no_file_exceeds_150_lines(self):
        """Check that no single file exceeds 150 lines (keep modules focused and modular)."""
        files = self._get_py_files()
        long_files = []
        for fname in files:
            lines = count_lines(fname)
            if lines > 150:
                long_files.append((fname, lines))

        self.assertEqual(
            len(long_files), 0,
            "These files are too long (over 150 lines):\n"
            + "\n".join(f"  {name}: {lines} lines" for name, lines in long_files)
            + "\n  The point of multi-module design is to keep each file\n"
            + "  focused. Split large files into smaller, themed modules."
        )

    def test_all_function_names_are_snake_case(self):
        """Check that all function names across all files follow snake_case convention."""
        files = self._get_py_files()
        snake_case = re.compile(r"^[a-z_][a-z0-9_]*$")
        bad = []
        for fname in files:
            tree = parse_file_ast(fname)
            if tree is None:
                continue
            for f in get_function_defs(tree):
                if not snake_case.match(f.name):
                    bad.append(f"{fname}: {f.name}")

        self.assertEqual(
            len(bad), 0,
            f"These function names are not snake_case:\n"
            + "\n".join(f"  {b}" for b in bad)
            + "\n  Python convention: 'createTree' -> 'create_tree'"
        )

    def test_all_functions_have_docstrings(self):
        """Check that every function in every file has a docstring."""
        files = self._get_py_files()
        missing = []
        for fname in files:
            tree = parse_file_ast(fname)
            if tree is None:
                continue
            for f in get_function_defs(tree):
                doc = get_docstring_from_node(f)
                if not doc:
                    missing.append(f"{fname}: {f.name}()")

        self.assertEqual(
            len(missing), 0,
            f"These functions are missing docstrings:\n"
            + "\n".join(f"  {m}" for m in missing)
            + '\n  Every function needs a docstring:\n'
            + '    def my_func():\n'
            + '        """Brief description of what this function does."""'
        )

    def test_all_files_parse_without_errors(self):
        """Check that every .py file in the project parses without syntax errors."""
        files = self._get_py_files()
        errors = []
        for fname in files:
            source = read_source(fname)
            if source is None:
                continue
            try:
                ast.parse(source)
            except SyntaxError as e:
                errors.append(f"{fname} (line {e.lineno}): {e.msg}")

        self.assertEqual(
            len(errors), 0,
            "These files have syntax errors:\n"
            + "\n".join(f"  {e}" for e in errors)
            + "\n  Fix all syntax errors before submitting."
        )

    def test_modules_have_focused_purpose(self):
        """Check that each module's functions share a theme (soft check on module focus)."""
        files = self._get_py_files()
        # This is a soft check -- we just verify that each module with functions
        # has at least 2 functions (suggesting it has a focused set of utilities)
        # and that function names in the same file share common word stems.
        single_function_files = []
        for fname in files:
            tree = parse_file_ast(fname)
            if tree is None:
                continue
            funcs = get_function_defs(tree)
            # Only flag files that have exactly 1 function (suggests it
            # could be merged or the file needs more related functions)
            if len(funcs) == 1:
                single_function_files.append(fname)

        # This is a soft recommendation, not a hard fail
        if single_function_files and len(find_py_files()) > 3:
            self.fail(
                f"These module files have only 1 function each: {single_function_files}\n"
                f"  Each module should group related functions together.\n"
                f"  Consider adding more functions to these modules, or\n"
                f"  merging them with a related module."
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
            self.stream.write("  Outstanding! All checks passed!\n")
        elif self.successes >= self.total - 2:
            self.stream.write("  So close! Just a few things to tidy up.\n")
        else:
            self.stream.write("  Keep working on your toolkit -- you're learning a lot!\n")
        self.stream.write("=" * 60 + "\n")


class FriendlyRunner(unittest.TextTestRunner):
    """Test runner that uses the friendly summary."""

    def run(self, test):
        result = FriendlySummary(sys.stdout, True, self.verbosity)
        sys.stdout.write("\n" + "=" * 60 + "\n")
        sys.stdout.write("  Assignment 5: Multi-Module Maya Toolkit - Self-Check\n")
        sys.stdout.write("=" * 60 + "\n\n")
        test(result)
        result.printSummary()
        return result


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment05)
    runner = FriendlyRunner()
    runner.run(suite)
