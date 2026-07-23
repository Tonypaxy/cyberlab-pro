#!/usr/bin/env python3
"""CyberLab Pro v1.0"""
import sys, os, platform, tkinter as tk

sys.path.insert(0, os.path.dirname(__file__))
IS_TERMUX = os.path.exists('/data/data/com.termux/files/usr/bin/bash')

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
from modules.cve_lookup import CVELookup
from modules.payload_generator import PayloadGenerator
from modules.session_logger import SessionLogger
from modules.api_integrations import APIIntegrations
from modules.report_templates import ReportTemplates
from modules.encrypted_vault import EncryptedVault
from modules.network_mapper import NetworkMapper
from modules.wordlist_manager import WordlistManager
from modules.log_analyzer import LogAnalyzer
from modules.clipboard_sanitizer import ClipboardSanitizer
from modules.checksum_verifier import ChecksumVerifier
from modules.phishing_module import PhishingModule
from modules.dos_module import DoSModule
from modules.macro_recorder import MacroRecorder
from modules.hash_cracker import HashCracker
from modules.exploit_suggester import ExploitSuggester
from modules.wifi_audit import WiFiAudit
from modules.subdomain_finder import SubdomainFinder
from modules.port_scanner import PortScanner
from modules.vuln_scanner import VulnScanner
from modules.forensic_toolkit import ForensicToolkit
from modules.wireless_toolkit import WirelessToolkit
from modules.cloud_toolkit import CloudToolkit
from modules.database_toolkit import DatabaseToolkit
from modules.stego_toolkit import StegoToolkit

class CyberLabApp:
    def __init__(self):
        self.config = Config(); self.logger = CyberLogger(); self.db = Database()
        self.monitor = SystemMonitor(); self.detector = ToolDetector(); self.detector.detect_all()
        self.session = SessionManager(self.config, self.db)
        self.project_core = ProjectCore(self.db, self.logger)
        self.services = ServiceManager(self.logger); self.permissions = PermissionManager(self.logger)
        self.themes = ThemeLoader(); self.running = True; self.current_view = None; self._toolcenter = None

    def run(self):
        self.logger.log_startup()
        splash = SplashScreen(1.5); splash.show()
        
        self.root = tk.Tk()
        self.root.title(f"CyberLab Pro v{self.config.get('version')}")
        self.root.configure(bg='#1a1a2e')
        
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}+0+0" if IS_TERMUX else f"{int(sw*0.9)}x{int(sh*0.85)}")
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        
        # Statusbar bottom
        self.statusbar = StatusBar(self.root); self.statusbar.build()
        self.statusbar.frame.pack(side='bottom', fill='x')
        
        # Toolbar top
        self.toolbar = ToolBar(self.root, {
            "dashboard": lambda: self.navigate("dashboard"),
            "projects": lambda: self.navigate("projects"),
            "recon": lambda: self.navigate("recon"),
            "terminal": lambda: self.navigate("terminal"),
            "settings": lambda: self.navigate("settings")
        }, self._toggle_sidebar)
        self.toolbar.build()
        self.toolbar.frame.pack(side='top', fill='x')
        
        # Sidebar left
        self.sidebar = Sidebar(self.root, self.navigate); self.sidebar.build()
        self.sidebar.frame.pack(side='left', fill='y')
        
        # Content fills rest
        self.content = tk.Frame(self.root, bg='#1a1a2e')
        self.content.pack(side='left', fill='both', expand=True)
        
        self.notifications = NotificationManager(self.root)
        
        self.navigate(self.session.get_last_module() or "dashboard")
        self._update_stats()
        self.root.mainloop()

    def _toggle_sidebar(self):
        if self.sidebar.frame.winfo_ismapped():
            self.sidebar.frame.pack_forget()
        else:
            self.sidebar.frame.pack(side='left', fill='y', before=self.content)

    def notify(self, msg, t="info"):
        if self.notifications: self.notifications.show(msg, t)

    def navigate(self, cmd):
        if self.current_view == cmd: return
        self.current_view = cmd
        for w in self.content.winfo_children(): w.destroy()
        if self.sidebar: self.sidebar.set_active(cmd)
        if self.toolbar: self.toolbar.set_active(cmd)
        
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
            "cve": lambda: CVELookup(self.content, self.db, self.logger).build(),
            "payloads": lambda: PayloadGenerator(self.content, self.db, self.logger).build(),
            "sessions": lambda: SessionLogger(self.content, self.db, self.logger).build(),
            "api": lambda: APIIntegrations(self.content, self.db, self.logger).build(),
            "templates": lambda: ReportTemplates(self.content, self.db, self.logger).build(),
            "vault": lambda: EncryptedVault(self.content, self.db, self.logger).build(),
            "mapper": lambda: NetworkMapper(self.content, self.db, self.logger).build(),
            "wordlists": lambda: WordlistManager(self.content, self.db, self.logger).build(),
            "loganalyzer": lambda: LogAnalyzer(self.content, self.db, self.logger).build(),
            "sanitizer": lambda: ClipboardSanitizer(self.content, self.db, self.logger).build(),
            "checksum": lambda: ChecksumVerifier(self.content, self.db, self.logger).build(),
            "phishing": lambda: PhishingModule(self.content, self.db, self.logger, self.detector).build(),
            "dos": lambda: DoSModule(self.content, self.db, self.logger, self.detector).build(),
            "macro": lambda: MacroRecorder(self.content, self.db, self.logger).build(),
            "hashcrack": lambda: HashCracker(self.content, self.db, self.logger).build(),
            "exploits": lambda: ExploitSuggester(self.content, self.db, self.logger).build(),
            "wifi": lambda: WiFiAudit(self.content, self.db, self.logger).build(),
            "subdomains": lambda: SubdomainFinder(self.content, self.db, self.logger, self.detector).build(),
            "portscan": lambda: PortScanner(self.content, self.db, self.logger).build(),
            "vulnscan": lambda: VulnScanner(self.content, self.db, self.logger).build(),
            "forensics": lambda: ForensicToolkit(self.content, self.db, self.logger).build(),
            "wireless2": lambda: WirelessToolkit(self.content, self.db, self.logger).build(),
            "cloud": lambda: CloudToolkit(self.content, self.db, self.logger).build(),
            "databases": lambda: DatabaseToolkit(self.content, self.db, self.logger).build(),
            "stego": lambda: StegoToolkit(self.content, self.db, self.logger).build(),
            "settings": lambda: SettingsPanel(self.content, self.config, self.logger, self._apply_theme).build(),
        }
        if cmd in views: views[cmd](); self.db.log_activity('module_opened', cmd)
        self.statusbar.set_status(cmd.title())

    def _apply_theme(self, name):
        name = name or self.config.get('theme', 'dark')
        self.config.set('theme', name)
        if hasattr(self, 'root'): self.root.configure(bg=self.themes.get(name)['bg'])
        if hasattr(self, 'content'): self.content.configure(bg=self.themes.get(name)['bg'])

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
        self.config.save(); self.logger.log_shutdown(); self.db.close()
        self.root.destroy(); sys.exit(0)

if __name__ == "__main__":
    CyberLabApp().run()
