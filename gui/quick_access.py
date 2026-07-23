import tkinter as tk
import os, json

class QuickAccess:
    def __init__(self, parent, navigate_callback=None):
        self.parent = parent
        self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#16213e', height=30)
        self.favorites = []
        self._load()
    
    def _load(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'config', 'favorites.json')
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self.favorites = json.load(f)
            except: pass
        if not self.favorites:
            self.favorites = [
                ("Recon", "recon"), ("Terminal", "terminal"), ("Tool Center", "tools"),
                ("Exploits", "exploits"), ("Port Scan", "portscan"), ("Subdomains", "subdomains")
            ]
    
    def _save(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'config', 'favorites.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def build(self):
        self.frame.pack(side='bottom', fill='x', before=self.parent.winfo_children()[0])
        self.frame.pack_propagate(False)
        
        tk.Label(self.frame, text="Quick", font=('Courier', 9, 'bold'),
                fg='#ffaa00', bg='#16213e').pack(side='left', padx=8, pady=4)
        
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=3)
        
        for name, cmd in self.favorites:
            btn = tk.Button(self.frame, text=name, font=('Courier', 8),
                    fg='#00ccff', bg='#16213e', relief='flat', padx=8, pady=2,
                    activebackground='#0f3460', activeforeground='#00ff88',
                    command=lambda c=cmd: self._go(c))
            btn.pack(side='left', padx=1, pady=3)
        
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=3)
        
        tk.Button(self.frame, text="Edit", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='flat', padx=8,
                command=self._edit).pack(side='left', padx=3, pady=3)
    
    def _go(self, cmd):
        if self.navigate:
            self.navigate(cmd)
    
    def _edit(self):
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title("Edit Quick Access"); d.geometry("400x350")
        tk.Label(d, text="Edit Favorites (max 10)", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        # Remove buttons
        tk.Label(d, text="Click to remove:", font=('Courier', 9), fg='#888', bg='#1a1a2e').pack()
        for name, cmd in self.favorites:
            row = tk.Frame(d, bg='#16213e')
            row.pack(fill='x', padx=20, pady=1)
            tk.Label(row, text=name, font=('Courier', 9), fg='#00ff88', bg='#16213e').pack(side='left', padx=5)
            tk.Button(row, text="X", font=('Courier', 8), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                    command=lambda n=name: self._remove(n, d)).pack(side='right')
        
        # Add new
        tk.Label(d, text="Add module:", font=('Courier', 9), fg='#888', bg='#1a1a2e').pack(pady=(10,0))
        all_mods = [
            ("Dashboard","dashboard"),("Projects","projects"),("Tool Center","tools"),
            ("Recon","recon"),("Network","network"),("Web","web"),("SOC Monitor","soc"),
            ("Reports","reports"),("Evidence","evidence"),("Notes","notes"),
            ("Terminal","terminal"),("Plugins","plugins"),("CVE Lookup","cve"),
            ("Wordlist Gen","wordlist"),("Permissions","permissions"),("Payload Gen","payloads"),
            ("Session Log","sessions"),("API Lookup","api"),("Templates","templates"),
            ("Vault","vault"),("Net Map","mapper"),("Wordlists","wordlists"),
            ("Log Analyzer","loganalyzer"),("Sanitizer","sanitizer"),("Checksum","checksum"),
            ("Exploits","exploits"),("Subdomains","subdomains"),("Port Scan","portscan"),
            ("Forensics","forensics"),("Wireless","wireless2"),("Cloud","cloud"),
            ("Stego","stego"),("Resources","resources"),("Auto Recon","autorecon"),
            ("OSINT","osint"),("Passwords","passwords"),("Fuzzing","fuzzing"),
            ("Malware","malware"),("Reverse Eng","reverse"),("Social Eng","social"),
            ("Settings","settings")
        ]
        fav_cmds = [c for _,c in self.favorites]
        for name, cmd in all_mods:
            if cmd not in fav_cmds and len(self.favorites) < 10:
                row = tk.Frame(d, bg='#16213e')
                row.pack(fill='x', padx=20, pady=1)
                tk.Label(row, text=name, font=('Courier', 8), fg='#888', bg='#16213e').pack(side='left', padx=5)
                tk.Button(row, text="Add", font=('Courier', 7), fg='#000', bg='#00ff88', relief='flat', padx=6,
                        command=lambda n=name,c=cmd: self._add(n,c,d)).pack(side='right')
        
        tk.Button(d, text="Close", font=('Courier', 10), fg='#fff', bg='#666',
                relief='raised', padx=15, pady=5, command=d.destroy).pack(pady=10)
    
    def _add(self, name, cmd, dialog):
        self.favorites.append((name, cmd))
        self._save()
        dialog.destroy()
        self._edit()
    
    def _remove(self, name, dialog):
        self.favorites = [(n,c) for n,c in self.favorites if n != name]
        self._save()
        dialog.destroy()
        self._edit()
