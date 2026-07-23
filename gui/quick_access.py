import tkinter as tk

class QuickAccess:
    """Floating quick access toolbar for frequently used tools"""
    
    def __init__(self, parent, callbacks=None):
        self.parent = parent
        self.callbacks = callbacks or {}
        self.frame = tk.Frame(parent, bg='#16213e', height=32)
        self.favorites = []
        self._load_favorites()
    
    def _load_favorites(self):
        """Load saved favorites"""
        import os, json
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
    
    def _save_favorites(self):
        import os, json
        path = os.path.join(os.path.dirname(__file__), '..', 'config', 'favorites.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def build(self):
        self.frame.pack(side='bottom', fill='x', before=self.parent.winfo_children()[0])
        self.frame.pack_propagate(False)
        
        # Left handle
        tk.Label(self.frame, text="⚡ Quick", font=('Courier', 9, 'bold'),
                fg='#ffaa00', bg='#16213e').pack(side='left', padx=8, pady=4)
        
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=3)
        
        # Favorite buttons
        for name, cmd in self.favorites[:10]:
            btn = tk.Button(self.frame, text=name, font=('Courier', 8),
                    fg='#00ccff', bg='#16213e', relief='flat', padx=8, pady=2,
                    activebackground='#0f3460', activeforeground='#00ff88',
                    command=lambda c=cmd: self._navigate(c))
            btn.pack(side='left', padx=1, pady=3)
        
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=3)
        
        # Add/Edit button
        tk.Button(self.frame, text="+", font=('Courier', 10, 'bold'),
                fg='#000', bg='#ffaa00', relief='flat', padx=8,
                command=self._edit_favorites).pack(side='left', padx=3, pady=3)
        
        # System stats
        self.stats_label = tk.Label(self.frame, text="", font=('Courier', 7),
                fg='#888', bg='#16213e')
        self.stats_label.pack(side='right', padx=10)
    
    def _navigate(self, command):
        if command in self.callbacks:
            self.callbacks[command]()
    
    def _edit_favorites(self):
        """Open dialog to edit favorites"""
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title("Edit Quick Access"); d.geometry("500x400")
        
        tk.Label(d, text="Edit Quick Access Favorites", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        tk.Label(d, text="Drag to reorder (max 10). Click to remove.", font=('Courier', 9),
                fg='#888', bg='#1a1a2e').pack()
        
        # Available modules
        all_modules = [
            ("Dashboard","dashboard"),("Projects","projects"),("Tool Center","tools"),
            ("Recon","recon"),("Network","network"),("Web","web"),("SOC Monitor","soc"),
            ("Reports","reports"),("Evidence","evidence"),("Notes","notes"),
            ("Terminal","terminal"),("Plugins","plugins"),("CVE Lookup","cve"),
            ("Wordlist Gen","wordlist"),("Permissions","permissions"),("Payload Gen","payloads"),
            ("Session Log","sessions"),("API Lookup","api"),("Templates","templates"),
            ("Vault","vault"),("Net Map","mapper"),("Wordlists","wordlists"),
            ("Log Analyzer","loganalyzer"),("Sanitizer","sanitizer"),("Checksum","checksum"),
            ("Exploits","exploits"),("Subdomains","subdomains"),("Port Scan","portscan"),
            ("Vuln Scan","vulnscan"),("Forensics","forensics"),("Wireless","wireless2"),
            ("Cloud","cloud"),("Databases","databases"),("Stego","stego"),
            ("Resources","resources"),("Auto Recon","autorecon"),("OSINT","osint"),
            ("Passwords","passwords"),("Fuzzing","fuzzing"),("Malware","malware"),
            ("Reverse Eng","reverse"),("Social Eng","social"),("IR Tools","incident"),
            ("Crypto","crypto"),("Browser","browser"),("API Security","api"),
            ("Backup","backup"),
        ]
        
        # Current favorites
        tk.Label(d, text="Current Favorites:", font=('Courier', 10, 'bold'),
                fg='#ffaa00', bg='#1a1a2e').pack(anchor='w', padx=20, pady=(10,0))
        
        current_frame = tk.Frame(d, bg='#16213e', padx=10, pady=5)
        current_frame.pack(fill='x', padx=20, pady=5)
        
        for name, cmd in self.favorites:
            row = tk.Frame(current_frame, bg='#16213e')
            row.pack(fill='x', pady=1)
            tk.Label(row, text=name, font=('Courier', 9), fg='#00ff88', bg='#16213e').pack(side='left')
            tk.Button(row, text="X", font=('Courier', 8), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                    command=lambda n=name,c=cmd: self._remove_favorite(n,c,d)).pack(side='right')
        
        # Add new
        tk.Label(d, text="Add Module:", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#1a1a2e').pack(anchor='w', padx=20, pady=(10,0))
        
        add_frame = tk.Frame(d, bg='#16213e', padx=10, pady=5)
        add_frame.pack(fill='x', padx=20, pady=5)
        
        # Only show modules not already in favorites
        fav_cmds = [c for _,c in self.favorites]
        available = [(n,c) for n,c in all_modules if c not in fav_cmds]
        
        for name, cmd in available:
            row = tk.Frame(add_frame, bg='#16213e')
            row.pack(fill='x', pady=1)
            tk.Label(row, text=name, font=('Courier', 9), fg='#888', bg='#16213e').pack(side='left')
            tk.Button(row, text="Add", font=('Courier', 8), fg='#000', bg='#00ff88', relief='flat', padx=6,
                    command=lambda n=name,c=cmd: self._add_favorite(n,c,d)).pack(side='right')
        
        tk.Button(d, text="Save & Close", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=20, pady=8,
                command=lambda: [self._save_favorites(), self._rebuild(), d.destroy()]).pack(pady=15)
    
    def _add_favorite(self, name, cmd, dialog):
        if len(self.favorites) < 10:
            self.favorites.append((name, cmd))
            dialog.destroy()
            self._edit_favorites()
    
    def _remove_favorite(self, name, cmd, dialog):
        self.favorites = [(n,c) for n,c in self.favorites if c != cmd]
        dialog.destroy()
        self._edit_favorites()
    
    def _rebuild(self):
        for w in self.frame.winfo_children():
            w.destroy()
        self.build()
    
    def update_stats(self, cpu, ram, tools):
        self.stats_label.config(text=f"CPU:{cpu}% | RAM:{ram}% | Tools:{tools}")
