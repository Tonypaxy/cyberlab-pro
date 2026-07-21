import json
import os
from pathlib import Path
from typing import Any, Dict

class Config:
    def __init__(self, config_path=None):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = config_path or str(self.base_dir / "config" / "settings.json")
        self._config = {}
        self._defaults = {
            "version": "1.0.0", "theme": "dark", "first_run": True,
            "last_project": None, "window_geometry": "800x600",
            "auto_save": True, "log_level": "INFO"
        }
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
            else:
                self._config = self._defaults.copy()
                self.save()
        except:
            self._config = self._defaults.copy()
    
    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=4)
    
    def get(self, key, default=None):
        return self._config.get(key, self._defaults.get(key, default))
    
    def set(self, key, value):
        self._config[key] = value
        if self.get("auto_save", True):
            self.save()
