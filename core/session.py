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
            "open_tabs": [],
            "window_geometry": "800x600",
            "theme": "dark",
            "recovery_points": []
        }
        self._restore()

    def _restore(self):
        """Restore session from database"""
        try:
            last = self.db.get_last_session()
            if last:
                self.data.update(last)
                self.config.set('last_project', self.data.get('last_project',{}).get('name'))
                self.config.set('theme', self.data.get('theme','dark'))
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

    def add_open_tab(self, tab_name):
        if tab_name not in self.data.get("open_tabs", []):
            self.data["open_tabs"].append(tab_name)

    def remove_open_tab(self, tab_name):
        if tab_name in self.data.get("open_tabs", []):
            self.data["open_tabs"].remove(tab_name)

    def set_theme(self, theme):
        self.data["theme"] = theme
        self.config.set("theme", theme)

    def get_theme(self):
        return self.data.get("theme", "dark")

    def create_recovery_point(self, name="auto"):
        """Save current state as recovery point"""
        point = {
            "name": name,
            "time": time.time(),
            "module": self.data.get("last_module"),
            "project": self.data.get("last_project"),
            "theme": self.data.get("theme"),
            "geometry": self.config.get("window_geometry", "800x600")
        }
        self.data.setdefault("recovery_points", []).append(point)
        if len(self.data["recovery_points"]) > 10:
            self.data["recovery_points"] = self.data["recovery_points"][-10:]
        self._save()
        return point

    def get_recovery_points(self):
        return self.data.get("recovery_points", [])

    def restore_recovery_point(self, index):
        """Restore to a specific recovery point"""
        points = self.data.get("recovery_points", [])
        if 0 <= index < len(points):
            point = points[index]
            self.data["last_module"] = point.get("module", "dashboard")
            self.data["last_project"] = point.get("project")
            self.data["theme"] = point.get("theme", "dark")
            self.config.set("theme", point.get("theme", "dark"))
            if point.get("geometry"):
                self.config.set("window_geometry", point.get("geometry"))
            self._save()
            return True
        return False

    def _save(self):
        self.data["last_save"] = time.time()
        self.db.save_session(self.data)

    def save(self):
        self.create_recovery_point("shutdown")
        self._save()
