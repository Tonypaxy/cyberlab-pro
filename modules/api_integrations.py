
import tkinter as tk
from tkinter import ttk, messagebox
import json, os, threading, subprocess
from datetime import datetime
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class APIIntegrations(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.api_keys = self._load_keys()
    
    def _load_keys(self):
        key_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'api_keys.json')
        if os.path.exists(key_file):
            try:
                with open(key_file) as f: return json.load(f)
            except: pass
        return {"shodan": "", "virustotal": "", "otx": "", "haveibeenpwned": ""}
    
    def _save_keys(self):
        key_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'api_keys.json')
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, 'w') as f: json.dump(self.api_keys, f, indent=2)
    
    def build_content(self):
        self.add_title("API Integrations", "Shodan, VirusTotal, AlienVault OTX, HaveIBeenPwned")
        
        # API Keys section
        def keys_content(parent):
            apis = [
                ("Shodan", "shodan", "Get free key at https://account.shodan.io"),
                ("VirusTotal", "virustotal", "Get free key at https://virustotal.com/gui/my-apikey"),
                ("AlienVault OTX", "otx", "Get free key at https://otx.alienvault.com/api"),
                ("HaveIBeenPwned", "haveibeenpwned", "Get key at https://haveibeenpwned.com/API/Key"),
            ]
            self.key_entries = {}
            for name, key, help_text in apis:
                row = tk.Frame(parent, bg='#16213e', padx=8, pady=6)
                row.pack(fill='x', pady=2)
                tk.Label(row, text=name, font=('Courier', 10), fg='#00ccff', bg='#16213e', width=15, anchor='w').pack(side='left')
                e = tk.Entry(row, font=('Courier', 9), bg='#0f3460', fg='#fff', relief='flat', show='*')
                e.pack(side='left', fill='x', expand=True, padx=5)
                e.insert(0, self.api_keys.get(key, ''))
                self.key_entries[key] = e
                tk.Label(parent, text=f"    {help_text}", font=('Courier', 7), fg='#666', bg='#1a1a2e').pack(anchor='w', padx=25)
            
            tk.Button(parent, text="Save API Keys", font=('Courier', 10, 'bold'), fg='#000', bg='#00ff88',
                    relief='raised', padx=15, pady=6, command=self._save_api_keys).pack(pady=10)
        
        self.add_section("API Keys (Saved Locally)", keys_content, "key", default_open=True)
        
        # Shodan Lookup
        def shodan_content(parent):
            tk.Label(parent, text="IP or Search Query:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w')
            self.shodan_entry = tk.Entry(parent, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
            self.shodan_entry.pack(fill='x', pady=3)
            self.shodan_entry.insert(0, '8.8.8.8')
            bf = tk.Frame(parent, bg='#1a1a2e')
            bf.pack(fill='x', pady=5)
            for text, cmd in [("IP Lookup","ip"),("Search","search"),("Ports","ports"),("Vulns","vulns")]:
                tk.Button(bf, text=text, font=('Courier', 9), fg='#000', bg='#ff4444',
                        relief='flat', padx=10, command=lambda c=cmd: self._shodan_lookup(c)).pack(side='left', padx=2)
        
        self.add_section("Shodan Search", shodan_content, "eye")
        
        # VirusTotal Lookup
        def vt_content(parent):
            tk.Label(parent, text="Hash, URL, IP, or Domain:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w')
            self.vt_entry = tk.Entry(parent, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
            self.vt_entry.pack(fill='x', pady=3)
            bf = tk.Frame(parent, bg='#1a1a2e')
            bf.pack(fill='x', pady=5)
            for text, cmd in [("File Hash","hash"),("URL Scan","url"),("IP Reputation","ip"),("Domain","domain")]:
                tk.Button(bf, text=text, font=('Courier', 9), fg='#000', bg='#ffaa00',
                        relief='flat', padx=10, command=lambda c=cmd: self._vt_lookup(c)).pack(side='left', padx=2)
        
        self.add_section("VirusTotal Lookup", vt_content, "virus")
        
        # OTX Lookup
        def otx_content(parent):
            tk.Label(parent, text="IP, Domain, or Hash:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w')
            self.otx_entry = tk.Entry(parent, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
            self.otx_entry.pack(fill='x', pady=3)
            self.otx_entry.insert(0, 'example.com')
            bf = tk.Frame(parent, bg='#1a1a2e')
            bf.pack(fill='x', pady=5)
            for text, cmd in [("IP Reputation","ip"),("Domain","domain"),("File Hash","hash"),("URL","url")]:
                tk.Button(bf, text=text, font=('Courier', 9), fg='#000', bg='#00ccff',
                        relief='flat', padx=10, command=lambda c=cmd: self._otx_lookup(c)).pack(side='left', padx=2)
        
        self.add_section("AlienVault OTX", otx_content, "pulse")
        
        # Results area
        self.results_frame = tk.Frame(self.inner, bg='#1a1a2e')
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter API keys above, then search")
    
    def _save_api_keys(self):
        for key, entry in self.key_entries.items():
            self.api_keys[key] = entry.get().strip()
        self._save_keys()
        messagebox.showinfo("Saved", "API keys saved to config/api_keys.json")
    
    def _show_result(self, title, data):
        for w in self.results_frame.winfo_children(): w.destroy()
        
        if not data:
            tk.Label(self.results_frame, text="No results or API key required", font=('Courier', 10), fg='#888', bg='#1a1a2e').pack(pady=10)
            return
        
        tk.Label(self.results_frame, text=title, font=('Courier', 11, 'bold'), fg='#00ff88', bg='#1a1a2e').pack(anchor='w')
        
        t = tk.Text(self.results_frame, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat', wrap='word', height=15)
        t.pack(fill='both', expand=True, pady=5)
        
        if isinstance(data, dict):
            t.insert('end', json.dumps(data, indent=2))
        else:
            t.insert('end', str(data))
        
        self.status_label.config(text=f"Results loaded")
    
    def _shodan_lookup(self, cmd):
        query = self.shodan_entry.get().strip()
        key = self.api_keys.get('shodan', '')
        if not key:
            messagebox.showinfo("API Key", "Enter Shodan API key first. Get free key at https://account.shodan.io")
            return
        
        self.status_label.config(text=f"Querying Shodan: {query}...")
        
        def do():
            try:
                import urllib.request
                if cmd == 'ip':
                    url = f"https://api.shodan.io/shodan/host/{query}?key={key}"
                else:
                    url = f"https://api.shodan.io/shodan/host/search?key={key}&query={query}"
                req = urllib.request.Request(url, headers={'User-Agent': 'CyberLab/1.0'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read())
                self.frame.after(0, lambda: self._show_result(f"Shodan: {query}", data))
            except Exception as e:
                self.frame.after(0, lambda: self._show_result("Error", str(e)))
        threading.Thread(target=do, daemon=True).start()
    
    def _vt_lookup(self, cmd):
        query = self.vt_entry.get().strip()
        key = self.api_keys.get('virustotal', '')
        if not key:
            messagebox.showinfo("API Key", "Enter VirusTotal API key. Get free key at https://virustotal.com/gui/my-apikey")
            return
        
        self.status_label.config(text=f"Querying VirusTotal: {query}...")
        
        def do():
            try:
                import urllib.request
                endpoints = {'hash': f'files/{query}', 'url': f'urls/{query}', 'ip': f'ip_addresses/{query}', 'domain': f'domains/{query}'}
                url = f"https://www.virustotal.com/api/v3/{endpoints.get(cmd, cmd)}"
                req = urllib.request.Request(url, headers={'x-apikey': key, 'User-Agent': 'CyberLab/1.0'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read())
                self.frame.after(0, lambda: self._show_result(f"VirusTotal: {query}", data))
            except Exception as e:
                self.frame.after(0, lambda: self._show_result("Error", str(e)))
        threading.Thread(target=do, daemon=True).start()
    
    def _otx_lookup(self, cmd):
        query = self.otx_entry.get().strip()
        key = self.api_keys.get('otx', '')
        
        self.status_label.config(text=f"Querying OTX: {query}...")
        
        def do():
            try:
                import urllib.request
                endpoints = {'ip': f'general', 'domain': f'general', 'hash': f'general', 'url': f'general'}
                url = f"https://otx.alienvault.com/api/v1/indicators/{cmd}/{query}/{endpoints.get(cmd, 'general')}"
                req = urllib.request.Request(url, headers={'X-OTX-API-KEY': key, 'User-Agent': 'CyberLab/1.0'}) if key else urllib.request.Request(url, headers={'User-Agent': 'CyberLab/1.0'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read())
                self.frame.after(0, lambda: self._show_result(f"OTX: {query}", data))
            except Exception as e:
                self.frame.after(0, lambda: self._show_result("Error", str(e)))
        threading.Thread(target=do, daemon=True).start()
