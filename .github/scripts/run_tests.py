"""
Autograding script for GitHub Classroom.

Detects which assignments have been modified (compared to the previous commit)
and runs their test_assignment.py files. If no specific assignment changed,
runs all available tests.

Exit code 0 = all tests passed, 1 = at least one failed.
"""

import os
import subprocess
import sys
import glob


def get_changed_files():
    """Get files changed in the most recent commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        return []


def detect_changed_assignments(changed_files):
    """Figure out which assignment directories had changes."""
    assignments = set()
    for f in changed_files:
        if f.startswith("assignments/assignment"):
            # Extract: assignments/assignment01_scene_builder/file.py -> assignment01_scene_builder
            parts = f.split("/")
            if len(parts) >= 2:
                assignments.add(parts[1])
    return sorted(assignments)


def find_all_assignments():
    """Find all assignment directories that have a test file."""
    test_files = glob.glob("assignments/assignment*/test_assignment.py")
    return sorted(os.path.basename(os.path.dirname(t)) for t in test_files)


def run_test(assignment_dir):
    """Run test_assignment.py for a given assignment. Returns True if passed."""
    test_path = os.path.join("assignments", assignment_dir, "test_assignment.py")
    if not os.path.exists(test_path):
        print(f"  No test file found at {test_path}, skipping.")
        return True

    print(f"\n{'=' * 60}")
    print(f"  Running: {test_path}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [sys.executable, "test_assignment.py"],
        cwd=os.path.join("assignments", assignment_dir),
        timeout=60
    )
    return result.returncode == 0


def main():
    changed_files = get_changed_files()
    changed_assignments = detect_changed_assignments(changed_files)

    if changed_assignments:
        print(f"Detected changes in: {', '.join(changed_assignments)}")
        assignments_to_test = changed_assignments
    else:
        print("No specific assignment changes detected. Running all tests.")
        assignments_to_test = find_all_assignments()

    if not assignments_to_test:
        print("No assignments found to test.")
        sys.exit(0)

    results = {}
    for assignment in assignments_to_test:
        passed = run_test(assignment)
        results[assignment] = passed

    # Summary
    print(f"\n{'=' * 60}")
    print("  RESULTS SUMMARY")
    print(f"{'=' * 60}")

    all_passed = True
    for assignment, passed in results.items():
        status = "PASS" if passed else "FAIL"
        icon = "[+]" if passed else "[-]"
        print(f"  {icon} {assignment}: {status}")
        if not passed:
            all_passed = False

    total = len(results)
    passed_count = sum(1 for v in results.values() if v)
    print(f"\n  Score: {passed_count}/{total} assignments passing")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
