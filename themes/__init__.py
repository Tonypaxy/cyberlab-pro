"""CyberLab Pro - Theme System with Live Application"""
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
        if not self.themes:
            self.themes['dark'] = {
                "name": "Dark", "bg": "#1a1a2e", "fg": "#00ff88",
                "accent": "#16213e", "btn": "#0f3460", "text": "#ffffff",
                "secondary": "#aaa", "error": "#cc0000", "warning": "#ccaa00",
                "sidebar_bg": "#16213e", "toolbar_bg": "#0f3460",
                "card_bg": "#16213e", "input_bg": "#0f3460", "output_bg": "#0a0a0a"
            }
    
    def get(self, name):
        return self.themes.get(name.lower(), self.themes.get('dark'))
    
    def list(self):
        return list(self.themes.keys())
