#!/usr/bin/env python3
"""CyberLab Pro v1.0 - Cross-Platform Cybersecurity Workspace"""
import sys
import os
import platform
import tkinter as tk

def verify_environment():
    issues = []
    if sys.version_info < (3, 8): issues.append("Python 3.8+ required")
    if platform.system() == 'Linux' and not os.environ.get('DISPLAY'): os.environ['DISPLAY'] = ':0'
    base = os.path.dirname(os.path.abspath(__file__))
    for d in ['core', 'gui', 'modules', 'config', 'logs', 'database', 'plugins', 'themes', 'assets']:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    return len(issues) == 0, issues

ok, issues = verify_environment()
if not ok: print("Environment issues:", issues); sys.exit(1)

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
from modules.wordlist_gen import WordlistGenerator

class CyberLabApp:
    def __init__(self):
        self.config = Config()
        self.logger = CyberLogger()
        self.db = Database()
        self.monitor = SystemMonitor()
        self.detector = ToolDetector()
        if IS_LINUX: self.detector._search_paths = ['/usr/bin','/usr/local/bin','/snap/bin',os.path.expanduser('~/go/bin')]
        self.detector.detect_all()
        self.session = SessionManager(self.config, self.db)
        self.project_core = ProjectCore(self.db, self.logger)
        self.services = ServiceManager(self.logger)
        self.themes = ThemeLoader()
        self.permissions = PermissionManager(self.logger)
        self.running = True
        self.current_theme = None
        self.sidebar = None; self.content = None; self.current_view = None
        self.notifications = None; self._toolcenter = None

    def run(self):
        self.logger.log_startup()
        self.db.log_activity("startup", f"CyberLab Pro launched")
        splash = SplashScreen(1.5); splash.show()
        
        self.root = tk.Tk()
        self.root.title(f"🛡️ CyberLab Pro v{self.config.get('version')}")
        self.root.geometry(f"{int(self.root.winfo_screenwidth()*0.9)}x{int(self.root.winfo_screenheight()*0.85)}")
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        
        # Set window icon
        try:
            icon = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'assets', 'icon.png'))
            self.root.iconphoto(True, icon)
        except: pass
        
        # Apply theme
        self._apply_theme(self.config.get('theme', 'dark'))
        
        self.statusbar = StatusBar(self.root); self.statusbar.build()
        self.toolbar = ToolBar(self.root, {"dashboard": lambda: self.navigate("dashboard"),"projects": lambda: self.navigate("projects"),"recon": lambda: self.navigate("recon"),"terminal": lambda: self.navigate("terminal"),"settings": lambda: self.navigate("settings")}, self._toggle_sidebar)
        self.toolbar.build()
        self.sidebar = Sidebar(self.root, self.navigate); self.sidebar.build()
        self.content = tk.Frame(self.root, bg=self.current_theme['bg']); self.content.pack(side='left', fill='both', expand=True)
        self.notifications = NotificationManager(self.root)
        
        start = self.session.get_last_module() or "dashboard"
        self.navigate(start)
        self._update_stats()
        self.root.mainloop()

    def _apply_theme(self, name=None):
        name = name or self.config.get('theme', 'dark')
        self.current_theme = self.themes.get(name)
        self.config.set('theme', name)
        
        # Apply to root
        if hasattr(self, 'root'):
            self.root.configure(bg=self.current_theme['bg'])
        if hasattr(self, 'content'):
            self.content.configure(bg=self.current_theme['bg'])
        if hasattr(self, 'toolbar'):
            self.toolbar.frame.configure(bg=self.current_theme['toolbar_bg'])
        if hasattr(self, 'sidebar'):
            self.sidebar.frame.configure(bg=self.current_theme['sidebar_bg'])
        if hasattr(self, 'statusbar'):
            self.statusbar.frame.configure(bg=self.current_theme['toolbar_bg'])
        
        self.logger.app_logger.info(f"Theme applied: {name}")

    def _toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    def _toggle_sidebar(self):
        if self.sidebar: self.sidebar.toggle()
    def notify(self, msg, t="info"):
        if self.notifications: self.notifications.show(msg, t)

    def navigate(self, cmd):
        if self.current_view == cmd: return
        self.current_view = cmd; self.session.set_last_module(cmd)
        for w in self.content.winfo_children(): w.destroy()
        if self.sidebar: self.sidebar.set_active(cmd)
        if self.toolbar: self.toolbar.set_active(cmd)
        self.content.update_idletasks()
        
        t = self.current_theme
        views = {
            "dashboard": lambda: Dashboard(self.content, self.monitor, self.detector, self.db, self.config, self.navigate).build(),
            "projects": lambda: ProjectManager(self.content, self.db, self.logger, self.navigate).build(),
            "tools": lambda: [setattr(self, '_toolcenter', ToolCenter(self.content, self.detector, self.logger, self.navigate)), self._toolcenter.build()],
            "recon": lambda: ReconWorkspace(self.content, self.db, self.logger, self.detector, self.notify).build(),
            "network": lambda: NetworkWorkspace(self.content, self.db, self.logger).build(),
            "web": lambda: WebWorkspace(self.content, self.db, self.logger, self.detector).build(),
            "reports": lambda: ReportsModule(self.content, self.db, self.logger).build(),
            "evidence": lambda: EvidenceModule(self.content, self.db, self.logger).build(),
            "notes": lambda: NotePad(self.content, self.db, self.logger).build(),
            "terminal": lambda: Terminal(self.content, self.config, self._toolcenter.get_pending_install() if self._toolcenter else None).build(),
            "plugins": lambda: PluginsManager(self.content, self.config, self.logger).build(),
            "soc": lambda: SOCDashboard(self.content, self.monitor, self.detector, self.db, self.logger, self.notify).build(),
            "permissions": lambda: PermissionsView(self.content, self.permissions, self.logger, self.notify).build(),
            "wordlist": lambda: WordlistGenerator(self.content, self.db, self.logger).build(),
            "settings": lambda: SettingsPanel(self.content, self.config, self.logger, self._apply_theme).build(),
        }
        if cmd in views: views[cmd]()
        self.statusbar.set_status(cmd.title()); self.content.update()

    def _update_stats(self):
        if self.running:
            try:
                ram = self.monitor.get_ram_usage(); cpu = self.monitor.get_cpu_usage()
                storage = self.monitor.get_storage_info(); tools = self.detector.get_total_count()
                self.statusbar.set_tool_info(f"CPU:{cpu}% | RAM:{ram['percent']}% | Free:{storage['free']}GB | Tools:{tools}")
            except: pass
            self.root.after(3000, self._update_stats)

    def shutdown(self):
        self.running = False; self.services.stop_all(); self.session.save()
        self.config.save(); self.logger.log_shutdown()
        self.db.log_activity("shutdown", "CyberLab Pro closed"); self.db.close()
        self.root.destroy(); sys.exit(0)

if __name__ == "__main__":
    CyberLabApp().run()
