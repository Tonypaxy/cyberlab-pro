#!/usr/bin/env python3
"""CyberLab Pro v1.0 - Cross-Platform Cybersecurity Workspace"""
import sys
import os
import platform
import tkinter as tk

def verify_environment():
    issues = []
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    if platform.system() == 'Linux' and not os.environ.get('DISPLAY'):
        os.environ['DISPLAY'] = ':0'
    base = os.path.dirname(os.path.abspath(__file__))
    for d in ['core', 'gui', 'modules', 'config', 'logs', 'database', 'plugins', 'themes', 'assets']:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    return len(issues) == 0, issues

ok, issues = verify_environment()
if not ok:
    print("Environment issues:", issues)
    sys.exit(1)

sys.path.insert(0, os.path.dirname(__file__))

IS_TERMUX = os.path.exists('/data/data/com.termux/files/usr/bin/bash')
IS_LINUX = platform.system() == 'Linux' and not IS_TERMUX

from core.config import Config
from core.logger import CyberLogger
from core.database import Database
from core.system import SystemMonitor
from core.tools import ToolDetector
from core.session import SessionManager
from core.projects import ProjectCore
from core.services import ServiceManager
from core.permissions import PermissionManager
from gui.splash import SplashScreen
from gui.dashboard import Dashboard
from gui.sidebar import Sidebar
from gui.toolbar import ToolBar
from gui.statusbar import StatusBar
from gui.settings import SettingsPanel
from gui.notifications import NotificationManager
from themes import ThemeLoader
from modules.projects import ProjectManager
from modules.toolcenter import ToolCenter
from modules.notes.notepad import NotePad
from modules.terminal.terminal import Terminal
from modules.recon.recon import ReconWorkspace
from modules.network.network import NetworkWorkspace
from modules.web.web import WebWorkspace
from modules.reports.reports import ReportsModule
from modules.evidence.evidence import EvidenceModule
from modules.plugins_manager import PluginsManager
from modules.soc_dashboard import SOCDashboard
from modules.permissions_view import PermissionsView

class CyberLabApp:
    def __init__(self):
        self.config = Config()
        self.logger = CyberLogger()
        self.db = Database()
        self.monitor = SystemMonitor()
        self.detector = ToolDetector()
        
        if IS_LINUX:
            self.detector._search_paths = [
                '/usr/bin', '/usr/local/bin', '/usr/sbin',
                '/snap/bin', '/opt', os.path.expanduser('~/go/bin'),
                os.path.expanduser('~/.local/bin')
            ]
        
        self.detector.detect_all()
        self.session = SessionManager(self.config, self.db)
        self.project_core = ProjectCore(self.db, self.logger)
        self.services = ServiceManager(self.logger)
        self.themes = ThemeLoader()
        self.permissions = PermissionManager(self.logger)
        self.running = True
        self.sidebar = None
        self.content = None
        self.current_view = None
        self.notifications = None
        self._toolcenter = None

    def run(self):
        self.logger.log_startup()
        
        # Check permissions
        perms = self.permissions.check_all()
        self.logger.app_logger.info(f"Permissions: {perms}")
        
        last_project = self.session.get_last_project()
        last_module = self.session.get_last_module()
        self.db.log_activity("startup", f"CyberLab Pro v{self.config.get('version')} launched on {platform.system()}")

        splash = SplashScreen(duration=1.5)
        splash.show()

        self.root = tk.Tk()
        # Set icon
        try:
            icon = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "assets", "icon.png"))
            self.root.iconphoto(True, icon)
        except:
            pass

        self.root.title(f"🛡️ CyberLab Pro v{self.config.get('version')}")
        self.root.configure(bg='#1a1a2e')
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_w*0.9)}x{int(screen_h*0.85)}+{int(screen_w*0.05)}+{int(screen_h*0.05)}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.root.bind('<Escape>', lambda e: self.shutdown())
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())

        theme = self.themes.get(self.config.get('theme', 'dark'))
        self.root.configure(bg=theme['bg'])

        self.statusbar = StatusBar(self.root)
        self.statusbar.build()

        nav_callbacks = {
            "dashboard": lambda: self.navigate("dashboard"),
            "projects": lambda: self.navigate("projects"),
            "recon": lambda: self.navigate("recon"),
            "terminal": lambda: self.navigate("terminal"),
            "settings": lambda: self.navigate("settings")
        }
        self.toolbar = ToolBar(self.root, nav_callbacks, self._toggle_sidebar)
        self.toolbar.build()

        self.sidebar = Sidebar(self.root, self.navigate)
        self.sidebar.build()

        self.content = tk.Frame(self.root, bg=theme['bg'])
        self.content.pack(side='left', fill='both', expand=True)
        
        self.notifications = NotificationManager(self.root)

        start_module = last_module or "dashboard"
        self.navigate(start_module)
        self._update_stats()

        tools_count = self.detector.get_total_count()
        proj_name = last_project['name'] if last_project else None
        plat = "Termux" if IS_TERMUX else platform.system()
        if proj_name:
            self.statusbar.set_status(f"{plat} | Project: {proj_name} | {tools_count} tools")
        else:
            self.statusbar.set_status(f"{plat} | Ready | {tools_count} tools")

        self.root.mainloop()

    def _toggle_fullscreen(self):
        state = not self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', state)

    def _toggle_sidebar(self):
        if self.sidebar:
            self.sidebar.toggle()

    def notify(self, message, type="info"):
        if self.notifications:
            self.notifications.show(message, type)

    def _apply_theme(self, name=None):
        if name is None:
            name = self.config.get("theme", "dark")
        theme = self.themes.get(name)
        self.root.configure(bg=theme["bg"])
        self.content.configure(bg=theme["bg"])

    def navigate(self, command):
        if self.current_view == command:
            return
        
        self.current_view = command
        self.session.set_last_module(command)
        
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if self.sidebar:
            self.sidebar.set_active(command)
        if self.toolbar:
            self.toolbar.set_active(command)
        
        self.content.update_idletasks()
        
        if command == "dashboard":
            Dashboard(self.content, self.monitor, self.detector, self.db, self.config, self.navigate).build()
        elif command == "projects":
            ProjectManager(self.content, self.db, self.logger, self.navigate).build()
        elif command == "tools":
            self._toolcenter = ToolCenter(self.content, self.detector, self.logger, self.navigate)
            self._toolcenter.build()
        elif command == "recon":
            ReconWorkspace(self.content, self.db, self.logger, self.detector, self.notify).build()
        elif command == "network":
            NetworkWorkspace(self.content, self.db, self.logger).build()
        elif command == "web":
            WebWorkspace(self.content, self.db, self.logger, self.detector).build()
        elif command == "reports":
            ReportsModule(self.content, self.db, self.logger).build()
        elif command == "evidence":
            EvidenceModule(self.content, self.db, self.logger).build()
        elif command == "notes":
            NotePad(self.content, self.db, self.logger).build()
        elif command == "terminal":
            pending = None
            if self._toolcenter:
                pending = self._toolcenter.get_pending_install()
            Terminal(self.content, self.config, pending).build()
        elif command == "plugins":
            PluginsManager(self.content, self.config, self.logger).build()
        elif command == "soc":
            SOCDashboard(self.content, self.monitor, self.detector, self.db, self.logger, self.notify).build()
        elif command == "permissions":
            PermissionsView(self.content, self.permissions, self.logger, self.notify).build()
        elif command == "settings":
            SettingsPanel(self.content, self.config, self.logger, self._apply_theme).build()
        
        self.statusbar.set_status(command.title())
        self.content.update()

    def _update_stats(self):
        if self.running:
            try:
                ram = self.monitor.get_ram_usage()
                cpu = self.monitor.get_cpu_usage()
                storage = self.monitor.get_storage_info()
                tools = self.detector.get_total_count()
                self.statusbar.set_tool_info(f"CPU:{cpu}% | RAM:{ram['percent']}% | Free:{storage['free']}GB | Tools:{tools}")
            except:
                pass
            self.root.after(3000, self._update_stats)

    def shutdown(self):
        self.running = False
        self.services.stop_all()
        self.session.save()
        self.config.save()
        self.logger.log_shutdown()
        self.db.log_activity("shutdown", "CyberLab Pro closed")
        self.db.close()
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = CyberLabApp()
    app.run()
