"""
CyberLab Pro - CVE Vulnerability Lookup
Search CVEs by service name, version, or keyword.
Works offline with local database, online with NVD API.
"""
import tkinter as tk
from gui.scrollable import make_scrollable
from gui.scrollable_frame import create_scrollable
from tkinter import ttk, messagebox
import json
import os
import threading
import subprocess
from datetime import datetime

class CVELookup:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.cve_cache = {}
        self._load_cache()
    
    def _load_cache(self):
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'cache', 'cve_cache.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file) as f:
                    self.cve_cache = json.load(f)
            except:
                self.cve_cache = {}
    
    def _save_cache(self):
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'cache', 'cve_cache.json')
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(self.cve_cache, f, indent=2)
    
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        tk.Label(header, text="CVE Lookup", font=('Courier', 18, 'bold'),
                fg='#ff4444', bg='#1a1a2e').pack(side='left')
        
        # Search bar
        search_frame = tk.Frame(self.frame, bg='#16213e', padx=10, pady=10)
        search_frame.pack(fill='x', pady=5)
        
        tk.Label(search_frame, text="Search:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(side='left')
        self.search_entry = tk.Entry(search_frame, font=('Courier', 11), bg='#0f3460',
                fg='#fff', insertbackground='#fff', relief='flat')
        self.search_entry.pack(side='left', fill='x', expand=True, padx=10)
        self.search_entry.bind('<Return>', lambda e: self._search())
        self.search_entry.insert(0, 'e.g., Apache 2.4.49, CVE-2021-41773')
        
        tk.Button(search_frame, text="Search", font=('Courier', 10, 'bold'),
                fg='#000', bg='#ff4444', relief='raised', padx=15,
                command=self._search).pack(side='right', padx=5)
        
        # Quick buttons for common services
        quick_frame = tk.Frame(self.frame, bg='#1a1a2e')
        quick_frame.pack(fill='x', pady=5)
        
        common = [
            ("Apache", "apache"), ("Nginx", "nginx"), ("OpenSSH", "openssh"),
            ("MySQL", "mysql"), ("WordPress", "wordpress"), ("Tomcat", "tomcat"),
            ("PHP", "php"), ("Python", "python"), ("Docker", "docker"),
            ("Kubernetes", "kubernetes"), ("Windows", "windows"), ("Linux Kernel", "linux kernel")
        ]
        
        for name, query in common:
            tk.Button(quick_frame, text=name, font=('Courier', 8),
                    fg='#000', bg='#0f3460', relief='flat', padx=6, pady=2,
                    command=lambda q=query: self._quick_search(q)).pack(side='left', padx=2, pady=2)
        
        # Results area
        self.results_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.results_frame.pack(fill='both', expand=True)
        
        # Status
        self.status_label = tk.Label(self.frame, text="Enter a service name or CVE ID to search",
                font=('Courier', 9), fg='#888', bg='#1a1a2e')
        self.status_label.pack(fill='x', pady=3)
    
    def _quick_search(self, query):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, query)
        self._search()
    
    def _search(self):
        query = self.search_entry.get().strip()
        if not query or query == 'e.g., Apache 2.4.49, CVE-2021-41773':
            return
        
        for w in self.results_frame.winfo_children(): w.destroy()
        self.status_label.config(text=f"Searching: {query}...")
        
        # Check cache first
        if query.lower() in self.cve_cache:
            self._display_results(self.cve_cache[query.lower()])
            return
        
        def do_search():
            results = []
            online_ok = False
            
            # Try NVD API online
            try:
                import urllib.request
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}&resultsPerPage=15"
                req = urllib.request.Request(url, headers={'User-Agent': 'CyberLab/1.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                    for vuln in data.get('vulnerabilities', []):
                        cve = vuln.get('cve', {})
                        cve_id = cve.get('id', 'Unknown')
                        desc = cve.get('descriptions', [{}])[0].get('value', '')[:200]
                        metrics = cve.get('metrics', {})
                        cvss_data = metrics.get('cvssMetricV31', metrics.get('cvssMetricV30', [{}]))
                        score = cvss_data[0].get('cvssData', {}).get('baseScore', 'N/A') if cvss_data else 'N/A'
                        severity = cvss_data[0].get('cvssData', {}).get('baseSeverity', 'N/A') if cvss_data else 'N/A'
                        results.append({
                            'title': f"{cve_id}: {desc}", 'cve': cve_id,
                            'score': str(score), 'severity': severity,
                            'source': 'NVD Online', 'type': 'cve'
                        })
                    online_ok = True
            except:
                pass
            
            # Try searchsploit
            try:
                result = subprocess.run(['searchsploit', '--cve', query],
                        capture_output=True, text=True, timeout=10)
                if result.stdout.strip():
                    for line in result.stdout.split('\n'):
                        if line.strip() and '---' not in line:
                            results.append({'title': line.strip(), 'source': 'ExploitDB', 'type': 'exploit'})
            except:
                pass
            
            # Always add built-in DB (offline fallback)
            known = self._get_known_cves(query)
            for k in known:
                if not any(r.get('cve') == k.get('cve') for r in results):
                    results.append(k)
            
            # Mark source
            if not online_ok and not results:
                results.append({'title': 'Offline - showing built-in database results only', 'source': 'Info', 'type': 'info'})
            
            # Cache
            self.cve_cache[query.lower()] = results
            self._save_cache()
            self.frame.after(0, lambda: self._display_results(results))
        
        threading.Thread(target=do_search, daemon=True).start()
    
    def _get_known_cves(self, query):
        """Built-in known CVEs for common services"""
        q = query.lower()
        known = []
        
        cve_db = {
            'apache 2.4.49': [('CVE-2021-41773', 'Path traversal/RCE', '7.5', 'HIGH'), ('CVE-2021-42013', 'Path traversal', '9.8', 'CRITICAL')],
            'apache 2.4.50': [('CVE-2021-42013', 'Path traversal', '9.8', 'CRITICAL'), ('CVE-2021-41773', 'Path traversal/RCE', '7.5', 'HIGH')],
            'apache log4j': [('CVE-2021-44228', 'Log4Shell RCE', '10.0', 'CRITICAL'), ('CVE-2021-45046', 'Log4j DoS', '9.0', 'CRITICAL')],
            'openssh': [('CVE-2024-6387', 'RegreSSHion RCE', '8.1', 'HIGH'), ('CVE-2023-38408', 'SSH Agent RCE', '8.8', 'HIGH')],
            'nginx': [('CVE-2021-23017', 'DNS resolver off-by-one', '7.7', 'HIGH'), ('CVE-2019-9511', 'HTTP/2 DoS', '7.5', 'HIGH')],
            'mysql': [('CVE-2023-21980', 'MySQL Client RCE', '7.5', 'HIGH'), ('CVE-2022-21497', 'Oracle MySQL DoS', '7.5', 'HIGH')],
            'wordpress': [('CVE-2024-28000', 'WP Password Reset', '9.8', 'CRITICAL'), ('CVE-2023-5360', 'WP File Upload', '7.2', 'HIGH')],
            'tomcat': [('CVE-2024-21733', 'Tomcat Request Smuggling', '7.5', 'HIGH'), ('CVE-2023-46589', 'Tomcat Request Smuggling', '7.5', 'HIGH')],
            'php': [('CVE-2024-4577', 'PHP CGI RCE', '9.8', 'CRITICAL'), ('CVE-2024-2961', 'PHP Buffer Overflow', '9.8', 'CRITICAL')],
            'docker': [('CVE-2024-21626', 'Docker runc escape', '8.6', 'HIGH'), ('CVE-2023-28842', 'Docker API bypass', '7.5', 'HIGH')],
            'kubernetes': [('CVE-2023-5528', 'K8s Privilege Escalation', '8.8', 'HIGH'), ('CVE-2023-3676', 'K8s Command Injection', '8.8', 'HIGH')],
            'linux kernel': [('CVE-2024-1086', 'Kernel Use-After-Free', '7.8', 'HIGH'), ('CVE-2023-32233', 'Netfilter UAF', '7.8', 'HIGH')],
            'windows': [('CVE-2024-30088', 'Windows Kernel EoP', '7.8', 'HIGH'), ('CVE-2024-21413', 'Outlook RCE', '9.8', 'CRITICAL')],
            'python': [('CVE-2023-24329', 'Python URL bypass', '7.5', 'HIGH'), ('CVE-2022-45061', 'Python DoS', '7.5', 'HIGH')],
        }
        
        for key, cves in cve_db.items():
            if key in q:
                for cve_id, desc, score, sev in cves:
                    known.append({'title': f"{cve_id}: {desc}", 'cve': cve_id, 'score': score, 'severity': sev, 'source': 'Built-in DB', 'type': 'cve'})
        
        return known
    
    def _display_results(self, results):
        for w in self.results_frame.winfo_children(): w.destroy()
        
        if not results:
            self.status_label.config(text="No results found. Try a different search term.")
            tk.Label(self.results_frame, text="No CVEs found.\nTry searching for: Apache, Nginx, SSH, MySQL, WordPress, etc.",
                    font=('Courier', 11), fg='#888', bg='#1a1a2e', justify='center').pack(expand=True)
            return
        
        self.status_label.config(text=f"Found {len(results)} results")
        
        canvas = tk.Canvas(self.results_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.results_frame, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas, bg='#1a1a2e')
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for r in results:
            self._result_card(sf, r)
    
    def _result_card(self, parent, result):
        sev_colors = {'CRITICAL': '#ff0000', 'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#00ff88', 'N/A': '#888'}
        color = sev_colors.get(result.get('severity', 'N/A'), '#888')
        
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        card.pack(fill='x', padx=5, pady=2)
        
        info = tk.Frame(card, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=12, pady=8)
        
        # CVE ID and score
        header_text = result.get('cve', result.get('title', 'Unknown')[:30])
        score = result.get('score', '')
        sev = result.get('severity', '')
        
        header_row = tk.Frame(info, bg='#16213e')
        header_row.pack(fill='x')
        tk.Label(header_row, text=header_text, font=('Courier', 10, 'bold'),
                fg=color, bg='#16213e').pack(side='left')
        if score:
            tk.Label(header_row, text=f" {score} {sev}", font=('Courier', 9, 'bold'),
                    fg=color, bg='#16213e').pack(side='left', padx=5)
        tk.Label(header_row, text=f" [{result.get('source', '')}]", font=('Courier', 8),
                fg='#666', bg='#16213e').pack(side='right')
        
        # Description
        if 'title' in result:
            tk.Label(info, text=result['title'][:120], font=('Courier', 8),
                    fg='#aaa', bg='#16213e', wraplength=500).pack(anchor='w')
        
        actions = tk.Frame(card, bg='#16213e')
        actions.pack(side='right', padx=12, pady=8)
        
        cve_id = result.get('cve', '')
        if cve_id:
            tk.Button(actions, text="Copy", font=('Courier', 8),
                    fg='#000', bg='#00ccff', relief='flat', padx=8,
                    command=lambda c=cve_id: self._copy(c)).pack(pady=1)
            tk.Button(actions, text="NVD", font=('Courier', 8),
                    fg='#000', bg='#ffaa00', relief='flat', padx=8,
                    command=lambda c=cve_id: self._open_nvd(c)).pack(pady=1)
            tk.Button(actions, text="ExploitDB", font=('Courier', 8),
                    fg='#fff', bg='#cc0000', relief='flat', padx=8,
                    command=lambda c=cve_id: self._search_exploitdb(c)).pack(pady=1)
    
    def _copy(self, text):
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(text)
            messagebox.showinfo("Copied", f"Copied: {text}")
        except:
            pass
    
    def _open_nvd(self, cve_id):
        try:
            subprocess.Popen(['termux-open', f'https://nvd.nist.gov/vuln/detail/{cve_id}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            messagebox.showinfo("NVD", f"Open in browser:\nhttps://nvd.nist.gov/vuln/detail/{cve_id}")
    
    def _search_exploitdb(self, cve_id):
        try:
            result = subprocess.run(['searchsploit', '--cve', cve_id],
                    capture_output=True, text=True, timeout=10)
            if result.stdout.strip():
                dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
                dialog.title(f"ExploitDB: {cve_id}"); dialog.geometry("600x400")
                tk.Label(dialog, text=f"ExploitDB Results: {cve_id}", font=('Courier', 12, 'bold'),
                        fg='#ff4444', bg='#1a1a2e').pack(pady=10)
                text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat')
                text.pack(fill='both', expand=True, padx=10, pady=10)
                text.insert('1.0', result.stdout)
                text.config(state='disabled')
                tk.Button(dialog, text="Close", font=('Courier', 10), fg='#fff', bg='#666',
                        relief='raised', padx=15, pady=5, command=dialog.destroy).pack(pady=5)
            else:
                messagebox.showinfo("ExploitDB", f"No exploits found for {cve_id}")
        except:
            messagebox.showinfo("ExploitDB", f"Run: searchsploit --cve {cve_id}")

    def _display_results(self, results):
        for w in self.results_frame.winfo_children(): w.destroy()
        
        if not results:
            self.status_label.config(text="No results. Try Apache, Nginx, SSH, MySQL, WordPress...")
            tk.Label(self.results_frame, text="No CVEs found.\nTry: Apache 2.4.49, Nginx, OpenSSH, MySQL, WordPress, Tomcat, PHP, Docker, Kubernetes, Windows, Linux Kernel, Python",
                    font=('Courier', 11), fg='#888', bg='#1a1a2e', justify='center').pack(expand=True)
            return
        
        self.status_label.config(text=f"Found {len(results)} results")
        
        sf = create_scrollable(self.results_frame, bg='#1a1a2e')
        sf.pack(fill='both', expand=True)
        for r in results:
            self._result_card(sf.inner, r)
