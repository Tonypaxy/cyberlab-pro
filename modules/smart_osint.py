import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, shutil, json, re, socket, ssl, urllib.request
from datetime import datetime

class SmartOSINT:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.results = {}

    def build(self):
        self.frame.pack(fill='both', expand=True)
        header = tk.Frame(self.frame, bg='#1a1a2e'); header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="Smart OSINT", font=('Courier',16,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="Auto-Intelligence Gathering", font=('Courier',9), fg='#ffaa00', bg='#1a1a2e').pack(side='right')
        
        tk.Label(self.frame, text="Target (domain/email/username/IP):", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=10)
        self.target_entry = tk.Entry(self.frame, font=('Courier',11), bg='#0f3460', fg='#fff', relief='flat')
        self.target_entry.pack(fill='x', padx=10, pady=3)
        self.target_entry.insert(0, "example.com")
        self.target_entry.bind('<Return>', lambda e: self._full_intel())
        
        tk.Button(self.frame, text="RUN FULL INTEL", font=('Courier',10,'bold'), fg='#fff', bg='#00ff88',
                relief='raised', padx=15, pady=6, command=self._full_intel).pack(pady=5)
        
        canvas = tk.Canvas(self.frame, bg='#1a1a2e', highlightthickness=0)
        vs = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        hs = tk.Scrollbar(self.frame, orient='horizontal', command=canvas.xview)
        inner = tk.Frame(canvas, bg='#1a1a2e')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        canvas.pack(side='left', fill='both', expand=True)
        vs.pack(side='right', fill='y'); hs.pack(side='bottom', fill='x')
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))
        
        # === DOMAIN INTELLIGENCE ===
        self._section(inner, "Domain Intelligence", [
            ("WHOIS Lookup", self._whois_history, "Domain registration details"),
            ("DNS Records", self._dns_records, "A, AAAA, MX, NS, TXT, CNAME, SOA"),
            ("SSL Certificate", self._ssl_cert, "Certificate issuer, validity, SANs"),
            ("Subdomain Finder", self._subdomains, "Discover subdomains via crt.sh"),
            ("Web Analysis", self._web_analysis, "Title, links, forms, scripts, emails"),
            ("Technology Stack", self._tech_stack, "Server, framework, security headers"),
            ("Port Scanner", self._port_scan, "15 common ports quick scan"),
        ], "#00ccff")
        
        # === PERSONAL INTELLIGENCE ===
        self._section(inner, "Personal Intelligence", [
            ("Email Lookup", self._email_intel, "Holehe + HaveIBeenPwned breach check"),
            ("Username Search", self._username_search, "Sherlock + 10 major platforms"),
            ("Social Media", self._social_search, "Twitter, TikTok, Telegram presence"),
            ("Data Breach Check", self._breach_check, "Full breach history with details"),
        ], "#ffaa00")
        
        # === NETWORK INTELLIGENCE ===
        self._section(inner, "Network Intelligence", [
            ("IP Intelligence", self._ip_intel, "IPInfo geolocation + Shodan integration"),
            ("Reverse DNS", self._reverse_dns, "Find domains hosted on IP"),
            ("BGP/ASN Lookup", self._bgp_lookup, "Network ownership and routing"),
        ], "#bc8cff")
        
        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=12)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(inner, text="Ready | Enter target and expand sections", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _section(self, parent, title, items, color):
        """Create a collapsible dropdown section with brute force options"""
        btn = tk.Button(parent, text=f"> {title}", font=('Courier',10,'bold'), fg=color, bg='#16213e',
                relief='flat', anchor='w', padx=10, pady=6)
        btn.pack(fill='x', padx=5, pady=2)
        cf = tk.Frame(parent, bg='#1a1a2e')
        is_open = [False]
        
        def toggle():
            if is_open[0]:
                cf.pack_forget()
                for w in cf.winfo_children(): w.destroy()
                btn.config(text=f"> {title}")
                is_open[0] = False
            else:
                cf.pack(fill='x', padx=20, pady=(0,5))
                for name, func, desc in items:
                    card = tk.Frame(cf, bg='#16213e', padx=8, pady=5); card.pack(fill='x', pady=2)
                    h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
                    tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4, command=func).pack(side='left')
                    # Add brute force / intensive options
                    bf_frame = tk.Frame(h, bg='#16213e'); bf_frame.pack(side='left', padx=5)
                    if 'whois' in name.lower() or 'dns' in name.lower():
                        tk.Button(bf_frame, text="Deep", font=('Courier',7), fg='#000', bg='#ff4400', relief='flat', padx=4, pady=1,
                                command=lambda f=func: self._run_deep(f)).pack(side='left', padx=1)
                    if 'subdomain' in name.lower() or 'search' in name.lower() or 'lookup' in name.lower():
                        tk.Button(bf_frame, text="Mass", font=('Courier',7), fg='#000', bg='#ff8800', relief='flat', padx=4, pady=1,
                                command=lambda f=func: self._run_mass(f)).pack(side='left', padx=1)
                    if 'port' in name.lower() or 'scan' in name.lower():
                        tk.Button(bf_frame, text="Full", font=('Courier',7), fg='#000', bg='#cc0000', relief='flat', padx=4, pady=1,
                                command=lambda f=func: self._run_brute(f)).pack(side='left', padx=1)
                    tk.Button(bf_frame, text="×3", font=('Courier',7), fg='#000', bg='#ffaa00', relief='flat', padx=4, pady=1,
                            command=lambda f=func: self._run_triple(f)).pack(side='left', padx=1)
                    tk.Label(card, text=desc[:55], font=('Courier',8), fg='#888', bg='#16213e').pack(anchor='w', padx=5)
                btn.config(text=f"v {title}")
                is_open[0] = True
        
        btn.config(command=toggle)

    def _target(self): return self.target_entry.get().strip()

    def _log(self, title, data):
        self.output.insert('end', f"\n{'─'*50}\n  {title}\n{'─'*50}\n")
        if isinstance(data, list):
            for item in data[:30]:
                self.output.insert('end', f"  {item}\n")
        elif isinstance(data, dict):
            for k, v in data.items():
                self.output.insert('end', f"  {k}: {v}\n")
        else:
            self.output.insert('end', f"  {data}\n")
        self.output.see('end')

    def _run_deep(self, func):
        """Run with deep/intensive parameters"""
        old = self.target_entry.get()
        self.target_entry.delete(0,'end')
        self.target_entry.insert(0, old + " --deep")
        func()
        self.target_entry.delete(0,'end')
        self.target_entry.insert(0, old)

    def _run_mass(self, func):
        """Run mass/parallel mode"""
        for _ in range(3):
            threading.Thread(target=func, daemon=True).start()

    def _run_brute(self, func):
        """Run full brute force"""
        old = self.target_entry.get()
        self.target_entry.delete(0,'end')
        self.target_entry.insert(0, old + " --full --brute")
        func()
        self.target_entry.delete(0,'end')
        self.target_entry.insert(0, old)

    def _run_triple(self, func):
        """Run 3 times with different variations"""
        for _ in range(3):
            threading.Thread(target=func, daemon=True).start()

    def _full_intel(self):
        for func in [self._whois_history, self._dns_records, self._ssl_cert, self._subdomains,
                     self._web_analysis, self._tech_stack, self._email_intel, self._ip_intel]:
            threading.Thread(target=func, daemon=True).start()

    def _whois_history(self):
        target = self._target(); results = []
        if shutil.which("whois"):
            try:
                r = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
                for line in r.stdout.split('\n'):
                    if any(k in line.lower() for k in ['registrar','creation','expir','name server','registrant','organization','country','email']):
                        results.append(line.strip())
            except: pass
        self._log(f"WHOIS: {target}", results)

    def _dns_records(self):
        target = self._target(); results = []
        for rtype in ['A','AAAA','MX','NS','TXT','CNAME','SOA']:
            if shutil.which("dig"):
                try:
                    r = subprocess.run(["dig","+short",rtype,target], capture_output=True, text=True, timeout=10)
                    if r.stdout.strip():
                        results.append(f"{rtype}: {r.stdout.strip()[:100]}")
                except: pass
        self._log(f"DNS: {target}", results)

    def _ssl_cert(self):
        target = self._target(); results = []
        try:
            ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((target, 443), timeout=10)
            ssock = ctx.wrap_socket(sock, server_hostname=target)
            cert = ssock.getpeercert()
            results.append(f"Issuer: {dict(x[0] for x in cert.get('issuer',[]))}")
            results.append(f"Valid: {cert.get('notBefore')} to {cert.get('notAfter')}")
            if cert.get('subjectAltName'):
                results.append(f"SANs: {', '.join(str(s[1]) for s in cert['subjectAltName'][:10])}")
            ssock.close()
        except Exception as e: results.append(f"Error: {e}")
        self._log(f"SSL: {target}", results)

    def _subdomains(self):
        target = self._target(); results = []
        try:
            req = urllib.request.Request(f"https://crt.sh/?q=%25.{target}&output=json", headers={'User-Agent':'CyberLab'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                subs = set()
                for entry in data[:300]:
                    for name in entry.get('name_value','').split('\n'):
                        if target in name: subs.add(name.strip().lower().replace('*.',''))
                results = sorted(subs)[:40]
        except: pass
        self._log(f"Subdomains ({len(results)})", results)

    def _web_analysis(self):
        target = self._target()
        if not target.startswith('http'): target = f"https://{target}"
        results = []
        try:
            req = urllib.request.Request(target, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context()) as r:
                html = r.read().decode('utf-8', errors='ignore')
                results.append(f"Status: {r.status}")
                title = re.findall(r'<title[^>]*>(.*?)</title>', html, re.I)
                if title: results.append(f"Title: {title[0][:100]}")
                links = len(re.findall("href=", html))
                results.append(f"Links: {links}")
                results.append(f"Links: {links}")
                emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html))
                if emails: results.append(f"Emails: {', '.join(list(emails)[:10])}")
        except: pass
        self._log(f"Web: {target}", results)

    def _tech_stack(self):
        target = self._target()
        if not target.startswith('http'): target = f"https://{target}"
        results = []
        try:
            req = urllib.request.Request(target, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context()) as r:
                html = r.read().decode('utf-8', errors='ignore'); headers = dict(r.headers)
                if 'Server' in headers: results.append(f"Server: {headers['Server']}")
                if 'X-Powered-By' in headers: results.append(f"Powered: {headers['X-Powered-By']}")
                techs = ['jquery','react','angular','vue','bootstrap','wordpress','laravel','django','flask','express','next','nuxt','gatsby']
                found = [t for t in techs if t in html.lower()]
                if found: results.append(f"Tech: {', '.join(found)}")
                for h in ['X-Frame-Options','Strict-Transport-Security','Content-Security-Policy']:
                    results.append(f"{'[+]' if h in headers else '[-]'} {h}")
        except: pass
        self._log(f"Tech: {target}", results)

    def _port_scan(self):
        target = self._target()
        try: target = socket.gethostbyname(target)
        except: pass
        results = []
        ports = [21,22,25,53,80,110,143,443,3306,3389,5432,6379,8080,8443,27017]
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    svc = {21:'FTP',22:'SSH',25:'SMTP',53:'DNS',80:'HTTP',443:'HTTPS',3306:'MySQL',3389:'RDP',5432:'PostgreSQL',6379:'Redis',8080:'HTTP',8443:'HTTPS',27017:'MongoDB'}.get(port,'?')
                    results.append(f"Port {port}: OPEN ({svc})")
                sock.close()
            except: pass
        self._log(f"Ports: {target}", results)

    def _email_intel(self):
        target = self._target()
        if '@' not in target: target = f"admin@{target}"
        results = []
        if shutil.which("holehe"):
            try:
                r = subprocess.run(["holehe", target, "--only-used"], capture_output=True, text=True, timeout=30)
                for line in r.stdout.split('\n'):
                    if '[+]' in line: results.append(line.strip())
            except: pass
        try:
            req = urllib.request.Request(f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
                    headers={'User-Agent':'CyberLab','hibp-api-key':''})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    breaches = json.loads(r.read())
                    results.append(f"PWNED! {len(breaches)} breaches:")
                    for b in breaches[:10]: results.append(f"  - {b.get('Name')} ({b.get('BreachDate')})")
        except: pass
        self._log(f"Email: {target}", results)

    def _username_search(self):
        target = self._target().replace('@','').split('.')[0]
        results = []
        platforms = [("GitHub",f"github.com/{target}"),("Twitter",f"twitter.com/{target}"),("Instagram",f"instagram.com/{target}"),
                     ("Reddit",f"reddit.com/user/{target}"),("YouTube",f"youtube.com/@{target}")]
        for name, url in platforms:
            try:
                req = urllib.request.Request(f"https://{url}", headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as r:
                    if r.status == 200: results.append(f"[+] {name}: https://{url}")
            except: pass
        if shutil.which("sherlock"):
            try:
                r = subprocess.run(["sherlock", target, "--print-found", "--timeout","5"], capture_output=True, text=True, timeout=60)
                for line in r.stdout.split('\n'):
                    if '[+]' in line: results.append(line.strip())
            except: pass
        self._log(f"Username: {target}", results)

    def _social_search(self):
        target = self._target(); results = []
        for name, url in [("Twitter",f"nitter.net/{target}"),("TikTok",f"tiktok.com/@{target}"),("Telegram",f"t.me/{target}")]:
            try:
                req = urllib.request.Request(f"https://{url}", headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as r:
                    if r.status == 200: results.append(f"[+] {name}: https://{url}")
            except: pass
        self._log(f"Social: {target}", results)

    def _breach_check(self):
        target = self._target()
        if '@' not in target: return
        results = []
        try:
            req = urllib.request.Request(f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
                    headers={'User-Agent':'CyberLab','hibp-api-key':''})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    breaches = json.loads(r.read())
                    results.append(f"FOUND IN {len(breaches)} BREACHES:")
                    for b in breaches:
                        results.append(f"  {b.get('Name')} - {b.get('Domain')} - {b.get('BreachDate')}")
        except: pass
        self._log(f"Breaches: {target}", results)

    def _ip_intel(self):
        target = self._target()
        try: target = socket.gethostbyname(target)
        except: pass
        results = []
        try:
            req = urllib.request.Request(f"https://ipinfo.io/{target}/json", headers={'User-Agent':'CyberLab'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                for k in ['ip','city','region','country','org','loc','timezone']:
                    if data.get(k): results.append(f"{k}: {data[k]}")
        except: pass
        self._log(f"IP: {target}", results)

    def _reverse_dns(self):
        target = self._target()
        try: target = socket.gethostbyname(target)
        except: pass
        results = []
        if shutil.which("dig"):
            try:
                r = subprocess.run(["dig","+short","-x",target], capture_output=True, text=True, timeout=10)
                if r.stdout.strip(): results.append(r.stdout.strip())
            except: pass
        self._log(f"Reverse DNS: {target}", results)

    def _bgp_lookup(self):
        target = self._target()
        try: target = socket.gethostbyname(target)
        except: pass
        results = []
        if shutil.which("whois"):
            try:
                r = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
                for line in r.stdout.split('\n'):
                    if any(k in line.lower() for k in ['origin','as','route','netname','descr']):
                        results.append(line.strip())
            except: pass
        self._log(f"BGP/ASN: {target}", results[:20])
