"""CyberLab Pro - Theme System"""
import json
import os
from pathlib import Path

class ThemeLoader:
    def __init__(self):
        self.themes = {}
        self.theme_dir = Path(__file__).parent
        self._load_all()
    
    def _load_all(self):
        for f in self.theme_dir.glob('*.json'):
            try:
                with open(f) as fh:
                    theme = json.load(fh)
                    self.themes[theme['name'].lower()] = theme
            except:
                pass
    
    def get(self, name):
        return self.themes.get(name.lower(), self.themes.get('dark'))
    
    def list(self):
        return list(self.themes.keys())
