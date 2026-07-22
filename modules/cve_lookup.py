import tkinter as tk
from tkinter import messagebox
import json, os, threading, subprocess
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class CVELookup(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.cve_cache = {}
        self._load_cache()
    
    def _load_cache(self):
        f = os.path.join(os.path.dirname(__file__), '..', 'cache', 'cve_cache.json')
        if os.path.exists(f):
            try:
                with open(f) as fh: self.cve_cache = json.load(fh)
            except: pass
    
    def _save_cache(self):
        f = os.path.join(os.path.dirname(__file__), '..', 'cache', 'cve_cache.json')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w') as fh: json.dump(self.cve_cache, fh, indent=2)
    
    def build_content(self):
        self.add_title("CVE Lookup", "Search vulnerabilities by service name or CVE ID")
        
        # Search bar
        sf = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
        sf.pack(fill='x', padx=10, pady=5)
        self.search_entry = tk.Entry(sf, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.search_entry.insert(0, 'Apache 2.4.49, nginx, CVE-2021-41773...')
        self.search_entry.bind('<Return>', lambda e: self._search())
        tk.Button(sf, text="Search", font=('Courier', 10, 'bold'), fg='#000', bg='#ff4444', relief='raised', padx=15,
                command=self._search).pack(side='right')
        
        # Common services - VERTICAL dropdown
        def common_content(parent):
            services = [
                ("Apache", "apache"), ("Nginx", "nginx"), ("OpenSSH", "openssh"),
                ("MySQL", "mysql"), ("WordPress", "wordpress"), ("Tomcat", "tomcat"),
                ("PHP", "php"), ("Docker", "docker"), ("Kubernetes", "kubernetes"),
                ("Windows", "windows"), ("Linux Kernel", "linux kernel"), ("Python", "python"),
                ("Node.js", "nodejs"), ("Redis", "redis"), ("PostgreSQL", "postgresql"),
                ("MongoDB", "mongodb"), ("Jenkins", "jenkins"), ("GitLab", "gitlab"),
            ]
            for name, query in services:
                tk.Button(parent, text=name, font=('Courier', 9), fg='#00ccff', bg='#16213e',
                        relief='flat', anchor='w', padx=10, pady=3,
                        command=lambda q=query: self._quick(q)).pack(fill='x', pady=1)
        
        self.add_section("Common Services", common_content, "🔍", default_open=True)
        
        # Results section
        self.results_frame = tk.Frame(self.inner, bg=self.bg)
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter a service name or CVE ID to search")
    
    def _quick(self, query):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, query)
        self._search()
    
    def _search(self):
        query = self.search_entry.get().strip()
        if not query or 'e.g.' in query: return
        
        for w in self.results_frame.winfo_children(): w.destroy()
        self.status_label.config(text=f"Searching: {query}...")
        
        if query.lower() in self.cve_cache:
            self._show(self.cve_cache[query.lower()])
            return
        
        def do():
            results = self._known(query)
            try:
                import urllib.request
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}&resultsPerPage=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'CyberLab/1.0'})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                    for v in data.get('vulnerabilities', []):
                        c = v.get('cve', {})
                        results.append({'cve': c.get('id','?'), 'desc': c.get('descriptions',[{}])[0].get('value','')[:150],
                                'severity': 'HIGH', 'source': 'NVD'})
            except: pass
            try:
                r = subprocess.run(['searchsploit','--cve',query], capture_output=True, text=True, timeout=10)
                for l in r.stdout.split('\n'):
                    if l.strip() and '---' not in l: results.append({'desc': l.strip(), 'source': 'ExploitDB'})
            except: pass
            self.cve_cache[query.lower()] = results; self._save_cache()
            self.frame.after(0, lambda: self._show(results))
        threading.Thread(target=do, daemon=True).start()
    
    def _known(self, query):
        q = query.lower()
        db = {
            'apache 2.4.49': [('CVE-2021-41773','Path traversal/RCE','CRITICAL'),('CVE-2021-42013','Path traversal','CRITICAL')],
            'apache log4j': [('CVE-2021-44228','Log4Shell RCE','CRITICAL')],
            'openssh': [('CVE-2024-6387','RegreSSHion RCE','HIGH')],
            'nginx': [('CVE-2021-23017','DNS resolver off-by-one','HIGH')],
            'mysql': [('CVE-2023-21980','MySQL Client RCE','HIGH')],
            'wordpress': [('CVE-2024-28000','Password Reset','CRITICAL')],
            'tomcat': [('CVE-2024-21733','Request Smuggling','HIGH')],
            'php': [('CVE-2024-4577','CGI RCE','CRITICAL')],
            'docker': [('CVE-2024-21626','runc escape','HIGH')],
            'kubernetes': [('CVE-2023-5528','Privilege Escalation','HIGH')],
            'linux kernel': [('CVE-2024-1086','Use-After-Free','HIGH')],
            'windows': [('CVE-2024-30088','Kernel EoP','HIGH')],
        }
        r = []
        for k, cves in db.items():
            if k in q:
                for cid, d, s in cves: r.append({'cve':cid,'desc':d,'severity':s,'source':'Built-in'})
        return r
    
    def _show(self, results):
        for w in self.results_frame.winfo_children(): w.destroy()
        self.status_label.config(text=f"Found {len(results)} results")
        
        if not results:
            tk.Label(self.results_frame, text="No results found.\nTry: Apache, Nginx, SSH, MySQL, WordPress...",
                    font=('Courier', 10), fg='#888', bg=self.bg, justify='center').pack(pady=20)
            return
        
        for r in results[:20]:
            sev = r.get('severity','N/A')
            color = {'CRITICAL':'#ff0000','HIGH':'#ff4444','MEDIUM':'#ffaa00','LOW':'#00ff88'}.get(sev,'#888')
            cve_id = r.get('cve','')
            
            # Vertical card
            card = tk.Frame(self.results_frame, bg='#16213e', padx=12, pady=8)
            card.pack(fill='x', pady=2)
            
            if cve_id:
                h = tk.Frame(card, bg='#16213e')
                h.pack(fill='x')
                tk.Label(h, text=f"{cve_id}", font=('Courier', 10, 'bold'), fg=color, bg='#16213e').pack(side='left')
                tk.Label(h, text=f" {sev}", font=('Courier', 9, 'bold'), fg=color, bg='#16213e').pack(side='left', padx=5)
                tk.Label(h, text=f"[{r.get('source','')}]", font=('Courier', 8), fg='#666', bg='#16213e').pack(side='right')
            
            tk.Label(card, text=r.get('desc','')[:150], font=('Courier', 8), fg='#aaa', bg='#16213e',
                    wraplength=self.canvas.winfo_width()-60, justify='left').pack(anchor='w', pady=3)
            
            if cve_id:
                bf = tk.Frame(card, bg='#16213e')
                bf.pack(fill='x')
                tk.Button(bf, text="Copy", font=('Courier', 7), fg='#000', bg='#00ccff', relief='flat', padx=6,
                        command=lambda c=cve_id: self._copy(c)).pack(side='left', padx=1)
                tk.Button(bf, text="NVD", font=('Courier', 7), fg='#000', bg='#ffaa00', relief='flat', padx=6,
                        command=lambda c=cve_id: self._nvd(c)).pack(side='left', padx=1)
                tk.Button(bf, text="ExploitDB", font=('Courier', 7), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                        command=lambda c=cve_id: self._exploitdb(c)).pack(side='left', padx=1)
    
    def _copy(self, t):
        try: self.frame.clipboard_clear(); self.frame.clipboard_append(t); messagebox.showinfo("Copied", t)
        except: pass
    
    def _nvd(self, cid):
        try: subprocess.Popen(['termux-open',f'https://nvd.nist.gov/vuln/detail/{cid}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except: messagebox.showinfo("NVD",f'https://nvd.nist.gov/vuln/detail/{cid}')
    
    def _exploitdb(self, cid):
        try:
            r = subprocess.run(['searchsploit','--cve',cid], capture_output=True, text=True, timeout=10)
            d = tk.Toplevel(self.frame, bg='#1a1a2e')
            d.title(f"ExploitDB: {cid}"); d.geometry("600x400")
            tk.Label(d, text=f"ExploitDB: {cid}", font=('Courier',12,'bold'), fg='#ff4444', bg='#1a1a2e').pack(pady=10)
            t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
            t.pack(fill='both', expand=True, padx=10, pady=10)
            t.insert('1.0', r.stdout or 'No results')
            t.config(state='disabled')
            tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=5, command=d.destroy).pack(pady=5)
        except: messagebox.showinfo("ExploitDB", f"Run: searchsploit --cve {cid}")
