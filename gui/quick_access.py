import tkinter as tk
import os, json

class QuickAccess:
    def __init__(self, parent, navigate_callback=None):
        self.parent = parent
        self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#16213e', height=28)
        self.favorites = []
        self._load()
    
    def _load(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'config', 'favorites.json')
        if os.path.exists(p):
            try:
                with open(p) as f: self.favorites = json.load(f)
            except: pass
        if not self.favorites:
            self.favorites = [("Recon","recon"),("Terminal","terminal"),("Tools","tools"),("Exploits","exploits")]
    
    def _save(self):
        p = os.path.join(os.path.dirname(__file__), '..', 'config', 'favorites.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f: json.dump(self.favorites, f, indent=2)
    
    def build(self):
        self.frame.pack(side='bottom', fill='x', before=self.parent.winfo_children()[0])
        self.frame.pack_propagate(False)
        
        tk.Label(self.frame, text="Quick", font=('Courier',9,'bold'), fg='#ffaa00', bg='#16213e').pack(side='left', padx=6, pady=3)
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=2)
        
        for name, cmd in self.favorites:
            tk.Button(self.frame, text=name, font=('Courier',8), fg='#00ccff', bg='#16213e',
                    relief='flat', padx=8, pady=2, activebackground='#0f3460', activeforeground='#00ff88',
                    command=lambda c=cmd: self._go(c)).pack(side='left', padx=1, pady=2)
        
        tk.Frame(self.frame, bg='#ffaa00', width=1).pack(side='left', fill='y', padx=2)
        tk.Button(self.frame, text="Edit", font=('Courier',8), fg='#000', bg='#ffaa00', relief='flat', padx=6,
                command=self._edit).pack(side='left', padx=2, pady=2)
    
    def _go(self, cmd):
        if self.navigate: self.navigate(cmd)
    
    def _edit(self):
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title("Edit Favorites"); d.geometry("380x320")
        tk.Label(d, text="Edit Favorites", font=('Courier',12,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=8)
        
        tk.Label(d, text="Remove:", font=('Courier',9), fg='#888', bg='#1a1a2e').pack()
        for name, cmd in self.favorites:
            r = tk.Frame(d, bg='#16213e'); r.pack(fill='x', padx=15, pady=1)
            tk.Label(r, text=name, font=('Courier',9), fg='#00ff88', bg='#16213e').pack(side='left', padx=5)
            tk.Button(r, text="X", font=('Courier',8), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                    command=lambda n=name: self._remove(n,d)).pack(side='right')
        
        tk.Label(d, text="Add:", font=('Courier',9), fg='#888', bg='#1a1a2e').pack(pady=(8,0))
        mods = [("Dash","dashboard"),("Projects","projects"),("Tools","tools"),("Recon","recon"),
                ("Network","network"),("Web","web"),("SOC","soc"),("Reports","reports"),
                ("Evidence","evidence"),("Notes","notes"),("Terminal","terminal"),("Plugins","plugins"),
                ("CVE","cve"),("Wordlist","wordlist"),("Perms","permissions"),("Payloads","payloads"),
                ("Sessions","sessions"),("API","api"),("Templates","templates"),("Vault","vault"),
                ("NetMap","mapper"),("Wordlists","wordlists"),("Logs","loganalyzer"),("Sanitize","sanitizer"),
                ("Checksum","checksum"),("Exploits","exploits"),("Subdomains","subdomains"),
                ("Wireless","wireless2"),("Cloud","cloud"),("Stego","stego"),("Resources","resources"),
                ("AutoRecon","autorecon"),("OSINT","osint"),("Passwords","passwords"),("Fuzzing","fuzzing"),
                ("Malware","malware"),("Reverse","reverse"),("Social","social"),("Settings","settings")]
        favs = [c for _,c in self.favorites]
        for name, cmd in mods:
            if cmd not in favs and len(self.favorites) < 10:
                r = tk.Frame(d, bg='#16213e'); r.pack(fill='x', padx=15, pady=1)
                tk.Label(r, text=name, font=('Courier',8), fg='#888', bg='#16213e').pack(side='left', padx=5)
                tk.Button(r, text="Add", font=('Courier',7), fg='#000', bg='#00ff88', relief='flat', padx=6,
                        command=lambda n=name,c=cmd: self._add(n,c,d)).pack(side='right')
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='flat', padx=15, pady=5, command=d.destroy).pack(pady=8)
    
    def _add(self, name, cmd, d):
        self.favorites.append((name, cmd)); self._save(); d.destroy(); self._edit()
    def _remove(self, name, d):
        self.favorites = [(n,c) for n,c in self.favorites if n != name]; self._save(); d.destroy(); self._edit()
