import importlib
from pathlib import Path
from profilek.profiles import BaseProfile
import inspect
from types import ModuleType
import os


class PluginLoader:
    def __init__(self, plugins_dir_path: str) -> None:
        self._plugins_dir_path = plugins_dir_path
        self._plugins = self._discover_plugins_paths()

    def _discover_plugins_paths(self) -> dict[str, BaseProfile]:
        plugins = {}
        for file_name in os.listdir(self._plugins_dir_path):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]
                module_path = f"{self._plugins_dir_path}.{module_name}"
                module: ModuleType = importlib.import_module(module_path)
                plugins_classes = self._find_plugins(module)
                plugins.update(plugins_classes)
        return plugins

    @staticmethod
    def _find_plugins(module: ModuleType) -> dict[str, BaseProfile]:
        members = inspect.getmembers(module)
        classes = (
            m[1]
            for m in members
            if inspect.isclass(m[1])
            and issubclass(m[1], BaseProfile)
            and m[1] is not BaseProfile
        )
        class_mapping = {klass.__name__: klass for klass in classes}
        return class_mapping

    @property
    def plugins(self) -> dict[str, BaseProfile]:
        return self._plugins
