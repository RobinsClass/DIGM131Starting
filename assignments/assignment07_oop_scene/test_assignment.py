"""
Self-check tests for Assignment 7: Simple Class-Based Scene Tool.

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


def _get_classes(tree):
    """Return all ClassDef nodes in *tree*."""
    return [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]


def _get_functions(tree):
    """Return all top-level FunctionDef nodes (not methods)."""
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _is_pascal_case(name):
    """Return True if *name* looks like PascalCase (starts upper, no underscores)."""
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))


def _is_snake_case(name):
    """Return True if *name* looks like snake_case."""
    if name.startswith("_"):
        name = name.lstrip("_")
    return bool(re.match(r"^[a-z][a-z0-9_]*$", name)) if name else True


def _get_init_self_assignments(init_node):
    """Return names assigned via self.xxx = ... inside an __init__."""
    attrs = set()
    for node in ast.walk(init_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"):
                    attrs.add(target.attr)
    return attrs


def _has_docstring(node):
    """Return True if node (ClassDef or FunctionDef) has a docstring."""
    return (node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str))


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestAssignment07(unittest.TestCase):
    """Structural checks for Assignment 7 — OOP Scene Tool."""

    @classmethod
    def setUpClass(cls):
        cls._files = {}
        cls._skip_reasons = {}
        for fname in ("scene_classes.py", "main.py"):
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

    def test_01_scene_classes_exists(self):
        """Check that scene_classes.py exists and is valid Python."""
        source, tree = self._require("scene_classes.py")
        self.assertIsNotNone(tree)

    def test_02_main_exists(self):
        """Check that main.py exists and is valid Python."""
        source, tree = self._require("main.py")
        self.assertIsNotNone(tree)

    def test_03_at_least_two_classes(self):
        """Check for at least 2 class definitions in scene_classes.py."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        self.assertGreaterEqual(len(classes), 2,
                                f"Found {len(classes)} class(es). The assignment asks for at least 2. "
                                "Think about what scene elements you can model as classes!")

    def test_04_class_names_pascal_case(self):
        """Check that class names use PascalCase (e.g. SceneObject, LightRig)."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        bad = [c.name for c in classes if not _is_pascal_case(c.name)]
        self.assertEqual(len(bad), 0,
                         f"These class names are not PascalCase: {bad}. "
                         "PascalCase means each word starts with a capital letter, no underscores. "
                         "Example: MyClassName")

    def test_05_classes_have_init(self):
        """Check that every class has an __init__ method."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        missing = []
        for cls in classes:
            methods = [n for n in cls.body
                       if isinstance(n, ast.FunctionDef) and n.name == "__init__"]
            if not methods:
                missing.append(cls.name)
        self.assertEqual(len(missing), 0,
                         f"These classes have no __init__ method: {missing}. "
                         "The __init__ method sets up your object's initial state — it's essential!")

    def test_06_init_has_instance_attributes(self):
        """Check that each __init__ sets at least 3 instance attributes (self.xxx = ...)."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        too_few = []
        for cls in classes:
            for node in cls.body:
                if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                    attrs = _get_init_self_assignments(node)
                    if len(attrs) < 3:
                        too_few.append((cls.name, len(attrs)))
        self.assertEqual(len(too_few), 0,
                         "These classes have fewer than 3 instance attributes in __init__: "
                         + ", ".join(f"{name} ({n} attrs)" for name, n in too_few)
                         + ". Give your objects more properties to describe them!")

    def test_07_classes_have_methods_beyond_init(self):
        """Check that each class has at least 2 methods besides __init__."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        too_few = []
        for cls in classes:
            methods = [n for n in cls.body
                       if isinstance(n, ast.FunctionDef) and n.name != "__init__"]
            if len(methods) < 2:
                too_few.append((cls.name, len(methods)))
        self.assertEqual(len(too_few), 0,
                         "These classes need more methods (at least 2 besides __init__): "
                         + ", ".join(f"{name} ({n} extra methods)" for name, n in too_few)
                         + ". Methods define what your objects can DO!")

    def test_08_classes_have_docstrings(self):
        """Check that every class has a docstring."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        missing = [c.name for c in classes if not _has_docstring(c)]
        self.assertEqual(len(missing), 0,
                         f"These classes are missing docstrings: {missing}. "
                         "Add a triple-quoted string right after the 'class' line to describe it.")

    def test_09_methods_have_docstrings(self):
        """Check that all methods have docstrings."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        missing = []
        for cls in classes:
            for node in cls.body:
                if isinstance(node, ast.FunctionDef) and not _has_docstring(node):
                    missing.append(f"{cls.name}.{node.name}")
        self.assertEqual(len(missing), 0,
                         f"These methods are missing docstrings: {missing}. "
                         "Every method should have a short description of what it does.")

    def test_10_main_imports_scene_classes(self):
        """Check that main.py imports from scene_classes."""
        source, tree = self._require("main.py")
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and "scene_classes" in node.module:
                found = True
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if "scene_classes" in alias.name:
                        found = True
        self.assertTrue(found,
                        "main.py should import from scene_classes. "
                        "Example: 'from scene_classes import MyClass'")

    def test_11_main_creates_instances(self):
        """Check that main.py creates class instances (calls class constructors)."""
        source, tree = self._require("main.py")
        # Gather class names from scene_classes if available
        class_names = set()
        if "scene_classes.py" in self._files:
            sc_tree = self._files["scene_classes.py"][1]
            class_names = {c.name for c in _get_classes(sc_tree)}

        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        found = False
        for call in calls:
            if isinstance(call.func, ast.Name) and call.func.id in class_names:
                found = True
                break
            # Also accept Attr calls like module.ClassName
            if isinstance(call.func, ast.Attribute) and call.func.attr in class_names:
                found = True
                break
        if not class_names:
            # Can't verify without class names, check for any PascalCase call
            for call in calls:
                if isinstance(call.func, ast.Name) and _is_pascal_case(call.func.id):
                    found = True
                    break
        self.assertTrue(found,
                        "main.py should create instances of your classes. "
                        "Example: 'my_obj = MyClass(...)' — this is how you use the classes you built!")

    def test_12_instance_vars_snake_case(self):
        """Check that instance variable names (self.xxx) use snake_case."""
        source, tree = self._require("scene_classes.py")
        classes = _get_classes(tree)
        bad = []
        for cls in classes:
            for node in cls.body:
                if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                    attrs = _get_init_self_assignments(node)
                    for attr in attrs:
                        if not _is_snake_case(attr):
                            bad.append(f"{cls.name}.{attr}")
        self.assertEqual(len(bad), 0,
                         f"These instance variables are not snake_case: {bad}. "
                         "Use lowercase with underscores, e.g. self.my_variable")


# ---------------------------------------------------------------------------
# Runner with friendly summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Assignment 7 Self-Check: OOP Scene Tool")
    print("=" * 60)
    print()
    print("  These tests check your code STRUCTURE — they do NOT")
    print("  run your Maya commands. Use them to catch common")
    print("  issues before you submit.")
    print()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssignment07)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("-" * 60)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    total = result.testsRun - len(result.skipped)
    if total == 0:
        print("  No tests could run. Make sure scene_classes.py and")
        print("  main.py exist in the same folder as this test file.")
    elif passed == total:
        print(f"  Fantastic! All {passed}/{total} checks passed!")
        print("  Your OOP structure looks solid. Great work!")
    else:
        print(f"  {passed}/{total} checks passed.")
        print("  Review the messages above for tips on what to improve.")
        print("  Object-oriented programming takes practice — keep going!")
    print("-" * 60)
