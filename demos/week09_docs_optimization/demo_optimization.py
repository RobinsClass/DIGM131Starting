"""
DIGM 131 - Week 9 Demo: Performance & Optimization
====================================================
Maya Python scripts can be slow if written carelessly.  This demo
shows how to MEASURE performance and apply simple optimizations.
"""

import time
import maya.cmds as cmds

# ============================================================
# Helper: timing decorator
# ============================================================
def timed(label):
    """Return a simple context manager that prints elapsed time."""
    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self
        def __exit__(self, *args):
            elapsed = time.time() - self.start
            print(f"  [{label}] {elapsed:.4f} seconds")
    return Timer()


# ============================================================
# PART 1: Measuring with time.time()
# ============================================================
print("=" * 50)
print("PART 1 -- Basic timing")
print("=" * 50)

start = time.time()
for i in range(200):
    cmds.polyCube(name=f"timing_cube_{i}")
elapsed = time.time() - start
print(f"  Created 200 cubes in {elapsed:.4f}s")

# Clean up
cmds.delete(cmds.ls("timing_cube_*"))


# ============================================================
# PART 2: Querying in a loop -- SLOW vs FAST
# ============================================================
print("\n" + "=" * 50)
print("PART 2 -- Avoid repeated queries")
print("=" * 50)

# Setup: create objects to query
cubes = []
for i in range(300):
    c = cmds.polyCube(name=f"opt_cube_{i}")[0]
    cmds.move(i * 0.1, 0, 0, c)
    cubes.append(c)

# SLOW: query every cube's position one at a time in a loop,
# then query it AGAIN to check the y value -- two calls per cube.
with timed("SLOW -- double query per cube"):
    for c in cubes:
        pos = cmds.xform(c, q=True, ws=True, t=True)
        y = cmds.getAttr(c + ".translateY")  # redundant second call

# FAST: query once, reuse the result.
with timed("FAST -- single query, reuse result"):
    for c in cubes:
        pos = cmds.xform(c, q=True, ws=True, t=True)
        y = pos[1]  # already have it!

# Clean up
cmds.delete(cubes)


# ============================================================
# PART 3: Batching vs Per-Object Commands
# ============================================================
print("\n" + "=" * 50)
print("PART 3 -- Batching operations")
print("=" * 50)

cubes = [cmds.polyCube(name=f"batch_cube_{i}")[0] for i in range(200)]

# SLOW: select and move each cube individually
with timed("SLOW -- move one at a time"):
    for c in cubes:
        cmds.move(0, 5, 0, c, relative=True)

# Reset positions
for c in cubes:
    cmds.move(0, 0, 0, c)

# FAST: select all, then move in one call
with timed("FAST -- select all, move once"):
    cmds.select(cubes)
    cmds.move(0, 5, 0, relative=True)  # acts on selection

cmds.delete(cubes)


# ============================================================
# PART 4: Undo Chunking
# ============================================================
print("\n" + "=" * 50)
print("PART 4 -- Undo chunking")
print("=" * 50)

# Without chunking, every cmds call is its own undo step.
# The user would need to press Ctrl+Z hundreds of times.

# WITH chunking, the entire operation is ONE undo step.
with timed("Creating 100 cubes in one undo chunk"):
    cmds.undoInfo(openChunk=True)          # <-- start chunk
    try:
        for i in range(100):
            c = cmds.polyCube(name=f"undo_cube_{i}")[0]
            cmds.move(i * 0.5, 0, 0, c)
    finally:
        cmds.undoInfo(closeChunk=True)     # <-- end chunk (always!)

print("  Now Ctrl+Z will undo ALL 100 cubes at once.")
# Clean up
cmds.delete(cmds.ls("undo_cube_*"))


# ============================================================
# PART 5: Caching Expensive Lookups
# ============================================================
print("\n" + "=" * 50)
print("PART 5 -- Caching vs re-querying")
print("=" * 50)

cubes = [cmds.polyCube(name=f"cache_cube_{i}")[0] for i in range(200)]

# SLOW: call cmds.ls() inside the loop every iteration
with timed("SLOW -- cmds.ls() inside loop"):
    for i in range(50):
        all_cubes = cmds.ls("cache_cube_*")  # re-queries every time
        _ = len(all_cubes)

# FAST: call cmds.ls() once, reuse the list
with timed("FAST -- cmds.ls() once, reuse"):
    all_cubes = cmds.ls("cache_cube_*")      # query once
    for i in range(50):
        _ = len(all_cubes)

cmds.delete(cubes)


# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 50)
print("OPTIMIZATION CHEAT SHEET")
print("=" * 50)
print("""
  1. MEASURE first -- don't guess. Use time.time().
  2. Don't query the same attribute twice -- store the result.
  3. Batch operations: select many, act once.
  4. Wrap big operations in undo chunks.
  5. Cache expensive lookups (cmds.ls, listRelatives, etc.).
  6. Avoid building strings in tight loops (use f-strings or join).
""")
