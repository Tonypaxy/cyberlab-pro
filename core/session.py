import time
import json

class SessionManager:
    def __init__(self, config, database):
        self.config = config
        self.db = database
        self.data = {
            "start_time": time.time(),
            "last_project": None,
            "last_module": "dashboard",
            "open_windows": [],
            "preferences": {}
        }
        self._restore()
    
    def _restore(self):
        """Restore session from database"""
        try:
            last = self.db.get_last_session()
            if last:
                self.data.update(last)
        except:
            pass
    
    def set_last_project(self, project_id, name):
        self.data["last_project"] = {"id": project_id, "name": name}
        self.config.set("last_project", name)
        self._save()
    
    def get_last_project(self):
        return self.data.get("last_project")
    
    def set_last_module(self, module_name):
        self.data["last_module"] = module_name
        self._save()
    
    def get_last_module(self):
        return self.data.get("last_module", "dashboard")
    
    def add_window(self, name):
        if name not in self.data["open_windows"]:
            self.data["open_windows"].append(name)
    
    def set_preference(self, key, value):
        self.data["preferences"][key] = value
    
    def get_preference(self, key, default=None):
        return self.data["preferences"].get(key, default)
    
    def _save(self):
        self.data["last_save"] = time.time()
        self.db.save_session(self.data)
    
    def save(self):
        self._save()
