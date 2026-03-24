"""
DIGM 131 - Week 7 Demo: OOP Literacy Across Languages
======================================================
You will encounter classes in almost every language you touch in your
career: C# (Unity), GDScript (Godot), JavaScript (web/Node), etc.

The SYNTAX differs, but the CONCEPTS are the same:
  - A class defines a blueprint.
  - __init__ / constructor sets up new instances.
  - Methods are functions that belong to the class.
  - 'self' / 'this' refers to the current instance.

Below, each example shows the SAME simple "Enemy" class in multiple
languages (as comment blocks) next to the working Python version.
"""

# ============================================================
# THE PYTHON VERSION (this one actually runs in Maya)
# ============================================================
import maya.cmds as cmds


class Enemy:
    """A simple enemy with a name and health."""

    def __init__(self, name, health=100):
        self.name = name        # instance attribute
        self.health = health

    def take_damage(self, amount):
        """Reduce health by amount, minimum 0."""
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage -> HP: {self.health}")

    def is_alive(self):
        return self.health > 0


# Quick test
goblin = Enemy("Goblin", health=40)
goblin.take_damage(15)
print(f"Alive? {goblin.is_alive()}")


# ============================================================
# C# (Unity) -- the same class would look like this:
# ============================================================
CSHARP_EXAMPLE = """
// C# uses 'public class', typed variables, and a constructor
// whose name matches the class name.

public class Enemy {
    public string name;          // <-- typed attribute
    public int health;

    // Constructor -- same name as the class, no return type
    public Enemy(string name, int health = 100) {
        this.name = name;        // 'this' instead of 'self'
        this.health = health;
    }

    public void TakeDamage(int amount) {
        health = Mathf.Max(0, health - amount);
        Debug.Log(name + " took " + amount + " damage");
    }

    public bool IsAlive() {
        return health > 0;       // 'bool' instead of implicit
    }
}

// Usage:
// Enemy goblin = new Enemy("Goblin", 40);   // 'new' keyword required
// goblin.TakeDamage(15);
"""

# Pattern spotting -- C# vs Python:
#   public class Enemy          ->  class Enemy:
#   public Enemy(...)           ->  def __init__(self, ...):
#   this.name                   ->  self.name
#   public void TakeDamage(...) ->  def take_damage(self, ...):
#   new Enemy(...)              ->  Enemy(...)


# ============================================================
# JavaScript (ES6) -- the same class:
# ============================================================
JAVASCRIPT_EXAMPLE = """
// JavaScript uses 'class' and 'constructor' keywords.

class Enemy {
    constructor(name, health = 100) {
        this.name = name;        // 'this' again, like C#
        this.health = health;
    }

    takeDamage(amount) {         // no 'def', no 'self' param
        this.health = Math.max(0, this.health - amount);
        console.log(`${this.name} took ${amount} damage`);
    }

    isAlive() {
        return this.health > 0;
    }
}

// Usage:
// const goblin = new Enemy("Goblin", 40);
// goblin.takeDamage(15);
"""

# Pattern spotting -- JS vs Python:
#   constructor(...)     ->  def __init__(self, ...):
#   this.health          ->  self.health
#   takeDamage(amount)   ->  def take_damage(self, amount):
#   No type annotations  ->  Same! Both are dynamically typed.


# ============================================================
# GDScript (Godot) -- the same class:
# ============================================================
GDSCRIPT_EXAMPLE = """
# GDScript looks the MOST like Python -- indentation-based,
# 'func' instead of 'def', and '_init' instead of '__init__'.

class_name Enemy

var name: String               # typed with ':'
var health: int = 100

func _init(p_name: String, p_health: int = 100):
    name = p_name              # no 'self' needed in GDScript
    health = p_health

func take_damage(amount: int):
    health = max(0, health - amount)
    print(name, " took ", amount, " damage")

func is_alive() -> bool:
    return health > 0

# Usage:
# var goblin = Enemy.new("Goblin", 40)
# goblin.take_damage(15)
"""

# Pattern spotting -- GDScript vs Python:
#   class_name Enemy      ->  class Enemy:
#   func _init(...)       ->  def __init__(self, ...):
#   var name: String      ->  self.name = name
#   func take_damage(...) ->  def take_damage(self, ...):
#   Enemy.new(...)        ->  Enemy(...)


# ============================================================
# KEY TAKEAWAY
# ============================================================
# Every language has its own spelling, but the recipe is the same:
#   1. Declare a class.
#   2. Write a constructor to initialize instance data.
#   3. Write methods that use 'self' or 'this' to access that data.
#   4. Create instances and call methods on them.
# Once you understand one, you can READ all the others.
