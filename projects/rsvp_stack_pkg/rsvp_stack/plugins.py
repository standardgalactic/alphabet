import importlib, pkgutil, inspect
from types import ModuleType
from typing import Dict, Any

PLUGIN_REGISTRY: Dict[str, Dict[str, Any]] = {}

def load_plugins(package="rsvp_stack.modules"):
    pkg = importlib.import_module(package)
    for _, name, _ in pkgutil.iter_modules(pkg.__path__):
        try:
            mod = importlib.import_module(f"{package}.{name}")
            PLUGIN_REGISTRY[name.lower()] = {"module": mod}
            print(f"[plugin] loaded: {name}")
        except Exception as e:
            print(f"[plugin] failed: {name} -> {e}")