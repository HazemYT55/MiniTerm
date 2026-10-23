import importlib.util
from pathlib import Path

class PluginManager:
    def __init__(self, write):
        self.write = write
        self.plugins = {}
        self.folder = Path(__file__).parent / "plugins"
        self.folder.mkdir(exist_ok=True)

    def load_plugins(self):
        self.plugins.clear()
        for path in sorted(self.folder.glob("*.py")):
            if path.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(f"miniterm_plugin_{path.stem}", path)
                if spec is None or spec.loader is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not callable(getattr(module, "run", None)):
                    self.write(f"Skipped plugin {path.name}: missing run(args) function.")
                    continue
                self.plugins[path.stem.lower()] = module
            except Exception as exc:
                self.write(f"Plugin {path.name} failed to load: {exc}")
        if self.plugins:
            self.write(f"Loaded {len(self.plugins)} plugin(s). Type 'plugins' to list them.")

    def run_command(self, name, args):
        module = self.plugins.get(name)
        if module is None:
            return False
        try:
            result = module.run(args)
            if result is not None:
                self.write(result)
        except Exception as exc:
            self.write(f"Plugin '{name}' error: {exc}")
        return True

    def names(self):
        return sorted(self.plugins)
