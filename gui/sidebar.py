import tkinter as tk

class Sidebar:
    def __init__(self, parent, command_callback=None):
        self.parent = parent
        self.command_callback = command_callback
        self.frame = tk.Frame(parent, bg='#16213e', width=175)
        self.buttons = {}
        
        self.menu_items = [
            ("Dashboard", "dashboard"), ("Projects", "projects"), ("Tool Center", "tools"),
            ("Recon", "recon"), ("Network", "network"), ("Web", "web"),
            ("SOC Monitor", "soc"), ("Reports", "reports"), ("Evidence", "evidence"),
            ("Notes", "notes"), ("Terminal", "terminal"), ("Plugins", "plugins"),
            ("CVE Lookup", "cve"), ("Wordlist Gen", "wordlist"),
            ("Payload Gen", "payloads"),
            ("Sessions", "sessions"),
            ("API Lookup", "api"),
            ("Templates", "templates"),
            ("Vault", "vault"),
            ("Net Map", "mapper"),
            ("Wordlists", "wordlists"),
            ("Log Analyzer", "loganalyzer"),
            ("Sanitizer", "sanitizer"),
            ("Checksum", "checksum"),
            ("Phishing", "phishing"),
            ("DoS Tools", "dos"),
            ("Macro Rec", "macro"),
            ("Hash Crack", "hashcrack"),
            ("Exploits", "exploits"),
            ("WiFi Audit", "wifi"),
            ("Wireless", "wireless2"),
            ("Cloud", "cloud"),
            ("Databases", "databases"),
            ("Stego", "stego"),
            ("Resources", "resources"),
            ("Subdomains", "subdomains"),
            ("Port Scan", "portscan"),
            ("Vuln Scan", "vulnscan"),
            ("Forensics", "forensics"),
            ("Permissions", "permissions"), ("Settings", "settings")
        ]
    
    def build(self):
        self.frame.pack_propagate(False)
        
        tk.Label(self.frame, text="CyberLab Pro", font=('Courier', 11, 'bold'),
                fg='#00ff88', bg='#0f3460', height=3).pack(fill='x')
        
        for text, cmd in self.menu_items:
            btn = tk.Button(self.frame, text=text, font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', relief='flat', pady=6, padx=8,
                    anchor='w', width=22,
                    command=lambda c=cmd: self._on_click(c))
            btn.pack(fill='x', padx=3, pady=1)
            self.buttons[cmd] = btn
        
        tk.Label(self.frame, text="v1.0.0", font=('Courier', 7),
                fg='#555', bg='#16213e').pack(side='bottom', pady=3)
        
        self.set_active("dashboard")
    
    def set_active(self, command):
        for cmd, btn in self.buttons.items():
            btn.configure(fg='#00ccff', bg='#16213e')
        if command in self.buttons:
            self.buttons[command].configure(fg='#000', bg='#00ff88')
    
    def _on_click(self, command):
        self.set_active(command)
        if self.command_callback: self.command_callback(command)
