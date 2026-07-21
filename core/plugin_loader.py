"""CyberLab Pro - Plugin System"""
import os
import importlib.util
from pathlib import Path

class PluginLoader:
    def __init__(self, logger):
        self.logger = logger
        self.plugins = {}
        self.plugin_dir = Path(__file__).parent.parent / "plugins"
    
    def discover(self):
        """Discover available plugins"""
        self.plugins = {}
        if not self.plugin_dir.exists():
            return self.plugins
        
        for item in self.plugin_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                self.plugins[item.name] = {
                    'path': str(item),
                    'loaded': False,
                    'module': None
                }
            elif item.suffix == '.py' and item.name != '__init__.py':
                name = item.stem
                self.plugins[name] = {
                    'path': str(item),
                    'loaded': False,
                    'module': None
                }
        
        self.logger.app_logger.info(f"Plugins discovered: {list(self.plugins.keys())}")
        return self.plugins
    
    def load_plugin(self, name):
        """Load a specific plugin"""
        if name not in self.plugins:
            return None
        
        plugin_info = self.plugins[name]
        try:
            spec = importlib.util.spec_from_file_location(name, plugin_info['path'])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_info['loaded'] = True
            plugin_info['module'] = module
            self.logger.app_logger.info(f"Plugin loaded: {name}")
            return module
        except Exception as e:
            self.logger.log_error(f"plugin_{name}", e)
            return None
    
    def load_all(self):
        """Load all discovered plugins"""
        for name in self.plugins:
            self.load_plugin(name)
        return self.plugins
    
    def get_loaded_plugins(self):
        """Get list of successfully loaded plugins"""
        return {k: v for k, v in self.plugins.items() if v['loaded']}
