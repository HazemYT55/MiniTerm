import ast
import operator
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from plugin_manager import PluginManager

class CommandEngine:
    def __init__(self, write, root):
        self.write = write
        self.root = root
        self.history = []
        self.plugin_manager = PluginManager(write)

    def load_plugins(self):
        self.plugin_manager.load_plugins()

    def execute(self, line):
        self.history.append(line)
        parts = line.split()
        if not parts:
            return
        name, args = parts[0].lower(), parts[1:]
        builtins = {
            "help": self.help,
            "about": self.about,
            "clear": self.clear,
            "time": self.show_time,
            "open": lambda a: self.open_website(a),
            "echo": lambda a: self.write(" ".join(a)),
            "pwd": lambda a: self.write(str(Path.cwd())),
            "plugins": lambda a: self.list_plugins(),
            "calc": lambda a: self.calculate(a),
            "exit": lambda a: self.root.destroy(),
        }
        if name in builtins:
            try:
                builtins[name](args)
            except Exception as exc:
                self.write(f"Error: {exc}")
            return
        if self.plugin_manager.run_command(name, args):
            return
        self.write(f"Unknown command: {name}. Type 'help' for commands.")

    def help(self, _args):
        self.write(
            "Built-in commands:\n"
            "  help              Show this help\n"
            "  about             About MiniTerm\n"
            "  clear             Clear the screen\n"
            "  open <website>    Open a website in your browser\n"
            "  echo <text>       Print text\n"
            "  time              Show the current time\n"
            "  pwd               Show the current working directory\n"
            "  calc <expression> Calculate basic arithmetic\n"
            "  plugins           List loaded plugins\n"
            "  exit              Close MiniTerm\n"
            "\nCustom commands are Python plugins in the plugins folder."
        )

    def about(self, _args):
        self.write("MiniTerm v0.1 — a Linux-inspired terminal simulator, not a real shell.")

    def clear(self, _args):
        # Clear the output widget through the callback's attached app reference.
        if hasattr(self.write, "__self__"):
            owner = self.write.__self__
            if hasattr(owner, "output"):
                owner.output.configure(state="normal")
                owner.output.delete("1.0", "end")
                owner.output.configure(state="disabled")

    def show_time(self, _args):
        self.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def open_website(self, args):
        if not args:
            self.write("Usage: open <website>")
            return
        raw = args[0]
        if "://" not in raw:
            raw = "https://" + raw
        parsed = urlparse(raw)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            self.write("Please provide a valid http or https website.")
            return
        webbrowser.open(raw)
        self.write(f"Opening {raw}")

    def list_plugins(self):
        names = self.plugin_manager.names()
        self.write("Loaded plugins: " + (", ".join(names) if names else "none"))

    def calculate(self, args):
        if not args:
            self.write("Usage: calc <expression>")
            return
        try:
            result = safe_calculate(" ".join(args))
            self.write(str(result))
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            self.write(f"Cannot calculate: {exc}")

def safe_calculate(expression):
    """Evaluate arithmetic AST nodes only; never use eval() on user input."""
    operators = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.UAdd: operator.pos,
    }
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("exponent is too large")
            result = operators[type(node.op)](left, right)
            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("result is too large")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](visit(node.operand))
        raise ValueError("only basic arithmetic is supported")
    return visit(ast.parse(expression, mode="eval"))
