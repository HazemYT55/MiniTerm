import json
from pathlib import Path

DEFAULTS = {
    "background": "#101318",
    "foreground": "#e7eaf0",
    "accent": "#62d6a8",
    "input_background": "#1b2029"
}
CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return {**DEFAULTS, **data}
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULTS.copy()
