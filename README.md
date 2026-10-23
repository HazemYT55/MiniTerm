# MiniTerm

MiniTerm is a lightweight, Linux-inspired **terminal simulator** built with Python and Tkinter. It is not a real Linux shell and does not execute arbitrary operating-system commands.

## Requirements
- Python 3.10 or newer (Tkinter included in most Windows Python installations)

## Run
```bash
python main.py
```

## Commands
- `help`
- `about`
- `clear`
- `open youtube.com`
- `echo Hello world`
- `time`
- `pwd`
- `calc 2 + 3 * 4`
- `plugins`
- `hello Hazem`
- `exit`

## Add a custom command
Create `plugins/greet.py`:
```python
def run(args):
    name = " ".join(args) if args else "friend"
    return f"Hello, {name}!"
```
Restart MiniTerm and type `greet Hazem`. Plugin filenames become command names.

## Security warning
Python plugins are executable code. A plugin can perform actions with the same permissions as MiniTerm, so only install plugins from sources you trust. This first version does not sandbox plugins.

## Configuration
Copy the settings from `themes/default.json` to a `config.json` file beside `main.py` to customize colors.

## Tests
```bash
python -m unittest discover -s tests
```

## License
This project is prepared with an MIT License template. Before publishing, add your copyright holder name and the standard MIT license text in `LICENSE`.

## Conclusion

| Item | What is it? | How to use it |
|---|---|---|
| **Python + Tkinter** | Python runs the program, and Tkinter creates the desktop window. | Install Python from [python.org](https://www.python.org/downloads/windows/). To test Tkinter, run `python -m tkinter` in your real terminal (Command Prompt). |
| **`plugins/` folder** | Stores your custom commands. | Create a new Python file inside this folder, such as `com.py`. The filename becomes the command name: `com`. |
| **`def run(args):`** | The function MiniTerm calls when someone uses your custom command. | Start your plugin with `def run(args):`, then write the code that you want it to execute. |
| **`return`** | Sends a result back to MiniTerm to display. | For example, `return "Hello!"` displays `Hello!` in MiniTerm. |
| **`args`** | Contains the words typed after the command name. | If someone types `greet Hazem`, the argument list contains `Hazem`. |
| **Restart MiniTerm** | Loads your newly created plugin. | Save your Python file, close MiniTerm, and launch `main.py` again. Then type your command. |

### Example: Create your first custom command

**Step 1 — Create the file**

Inside the `plugins/` folder, create a file named `greet.py`.

**Step 2 — Write the code**

```python
def run(args):
    name = " ".join(args) if args else "friend"
    return f"Hello, {name}!"
```

**Step 3 — Save and run**

Save the file and restart MiniTerm.

**Step 4 — Try your command**

```text
guest@miniterm:~$ greet
Hello, friend!

guest@miniterm:~$ greet Hazem
Hello, Hazem!
```

Congratulations! You have created your first custom MiniTerm command.

### Create commands that do more

Your commands can do more than display text. With Python, you can build simple calculators, display information, format text, or create other useful features.

For example, this command displays a custom message:

```python
def run(args):
    return "Welcome to my custom MiniTerm command!"
```

Replace the message with your own idea and experiment with Python.

### Important notes

- The filename determines the command name. For example, `com.py` creates the `com` command.
- The plugin must contain a callable `run(args)` function.
- In this version, MiniTerm loads plugins when it starts, so restart the application after adding or editing a plugin.
- Python plugins can execute code with the same permissions as MiniTerm. Only run plugins you trust.
- MiniTerm is a terminal simulator inspired by Linux; it is not a real Linux shell.

**Keep learning. Keep building. Make MiniTerm yours!**


## Creator

| Name | Link / Credits |
|---|---|
| Lazem Hazem | [YouTube Channel](https://youtube.com/@lazemhazem) |
| AI Assistant | Thanks to ChatGPT for helping with the project! |

---

**MiniTerm — Learn. Build. Customize.**
