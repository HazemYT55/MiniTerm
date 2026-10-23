import tkinter as tk
from tkinter import scrolledtext
from command_engine import CommandEngine
from config import load_config

class MiniTermApp:
    def __init__(self):
        self.root = tk.Tk()
        self.config = load_config()
        self.root.title("MiniTerm")
        self.root.geometry("820x520")
        self.root.minsize(620, 380)
        self.root.configure(bg=self.config["background"])

        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled",
            bg=self.config["background"], fg=self.config["foreground"],
            insertbackground=self.config["foreground"],
            font=("Consolas", 11), borderwidth=0, padx=14, pady=12
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        bottom = tk.Frame(self.root, bg=self.config["background"])
        bottom.pack(fill=tk.X, padx=12, pady=(0, 12))
        self.prompt = tk.Label(
            bottom, text="guest@miniterm:~$", bg=self.config["background"],
            fg=self.config["accent"], font=("Consolas", 11)
        )
        self.prompt.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            bottom, bg=self.config["input_background"],
            fg=self.config["foreground"], insertbackground=self.config["foreground"],
            font=("Consolas", 11), relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0), ipady=7)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

        self.engine = CommandEngine(self.write, self.root)
        self.write("MiniTerm v0.1\nA customizable terminal simulator built with Python.\nType 'help' to see commands.\n")
        self.engine.load_plugins()

    def write(self, text):
        self.output.configure(state="normal")
        self.output.insert(tk.END, str(text) + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def submit(self, _event=None):
        command = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not command:
            return
        self.write(f"guest@miniterm:~$ {command}")
        self.engine.execute(command)

    def run(self):
        self.root.mainloop()
