from pathlib import Path
import json
import threading
#from .civit import Civit
import time
import os
from custom.OneButtonPrompt.utils import path_fixed, root_path_fixed

class PathManager:
    DEFAULT_PATHS = {
        "path_cache": root_path_fixed("../cache/"),
    }

    EXTENSIONS = [".pth", ".ckpt", ".bin", ".safetensors"]

    def __init__(self):
        self.paths = self.load_paths()
        self.model_paths = self.get_model_paths()
        self.default_model_names = self.get_default_model_names()
        self.update_all_model_names()

    def load_paths(self):
        paths = self.DEFAULT_PATHS.copy()
        settings_path = Path(path_fixed("settings/paths.json"))
        if settings_path.exists():
            with settings_path.open() as f:
                paths.update(json.load(f))
        for key in self.DEFAULT_PATHS:
            if key not in paths:
                paths[key] = self.DEFAULT_PATHS[key]
        with settings_path.open("w") as f:
            json.dump(paths, f, indent=2)
        return paths

    def get_abspath_folder(self, path):
        folder = self.get_abspath(path)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        return folder

    def get_abspath(self, path):
        return Path(path) if Path(path).is_absolute() else Path(__file__).parent / path

    def get_model_paths(self):
        return {
            "cache_path": self.get_abspath_folder(self.paths["path_cache"]),
        }
