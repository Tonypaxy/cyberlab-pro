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
        
        bf = tk.Frame(self.frame, bg='#1a1a2e'); bf.pack(fill='x', padx=10, pady=5)
        
        scans = [
            ("Full Intel", self._full_intel, "#00ff88"),
            ("Domain Intel", self._domain_intel, "#00ccff"),
            ("Email Intel", self._email_intel, "#ffaa00"),
            ("Username Search", self._username_search, "#ff4444"),
            ("IP Intelligence", self._ip_intel, "#bc8cff"),
            ("Social Media", self._social_search, "#ff00ff"),
            ("Tech Stack", self._tech_stack, "#d2991d"),
            ("Data Breach", self._breach_check, "#ff0000"),
            ("WHOIS History", self._whois_history, "#58a6ff"),
            ("DNS Records", self._dns_records, "#39c5cf"),
            ("SSL Certificate", self._ssl_cert, "#3fb950"),
            ("Subdomains", self._subdomains, "#ff8800"),
            ("Port Scan", self._port_scan, "#ff4444"),
            ("Web Analysis", self._web_analysis, "#00ccff"),
        ]
        
        for name, func, color in scans:
            tk.Button(bf, text=name, font=('Courier',9), fg='#000', bg=color, relief='flat', padx=8, pady=4, command=func).pack(side='left', padx=2)
        
        self.output = tk.Text(self.frame, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=15)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(self.frame, text="Ready | Enter target and click scan", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _target(self): return self.target_entry.get().strip()

    def _log(self, title, data):
        self.output.insert('end', f"\n{'='*60}\n  {title}\n{'='*60}\n")
        if isinstance(data, list):
            for item in data[:30]:
                self.output.insert('end', f"  {item}\n")
        elif isinstance(data, dict):
            for k, v in data.items():
                self.output.insert('end', f"  {k}: {v}\n")
        else:
            self.output.insert('end', f"  {data}\n")
        self.output.see('end')

    def _full_intel(self):
        for func in [self._domain_intel, self._email_intel, self._ip_intel, self._tech_stack, 
                     self._dns_records, self._ssl_cert, self._subdomains, self._web_analysis]:
            threading.Thread(target=func, daemon=True).start()

    def _domain_intel(self):
        target = self._target()
        self.status.config(text=f"Gathering domain intel on {target}...")
        results = []
        
        # WHOIS
        if shutil.which("whois"):
            try:
                r = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
                for line in r.stdout.split('\n'):
                    if any(k in line.lower() for k in ['registrar','creation','expir','name server','registrant','organization','country','email']):
                        results.append(line.strip())
            except: pass
        
        # BuiltWith/Technology
        try:
            req = urllib.request.Request(f"https://builtwith.com/{target}", headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                html = r.read().decode()
                techs = re.findall(r'<a[^>]*>(jQuery|WordPress|Apache|Nginx|Cloudflare|AWS|Google|PHP|React|Angular|Vue|Bootstrap)[^<]*</a>', html, re.I)
                if techs:
                    results.append(f"Technologies: {', '.join(set(techs))}")
        except: pass
        
        self._log(f"Domain Intelligence: {target}", results)
        self.status.config(text="Domain intel complete")

    def _email_intel(self):
        target = self._target()
        if '@' not in target: target = f"admin@{target}"
        self.status.config(text=f"Checking email: {target}...")
        results = []
        
        # Holehe
        if shutil.which("holehe"):
            try:
                r = subprocess.run(["holehe", target, "--only-used"], capture_output=True, text=True, timeout=30)
                for line in r.stdout.split('\n'):
                    if '[+]' in line: results.append(line.strip())
            except: pass
        
        # HaveIBeenPwned
        try:
            req = urllib.request.Request(f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
                    headers={'User-Agent':'CyberLab','hibp-api-key':''})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    breaches = json.loads(r.read())
                    results.append(f"PWNED! Found in {len(breaches)} breaches:")
                    for b in breaches[:10]:
                        results.append(f"  - {b.get('Name','?')} ({b.get('BreachDate','?')})")
        except: results.append("HaveIBeenPwned: No breaches or API error")
        
        self._log(f"Email Intelligence: {target}", results)
        self.status.config(text="Email intel complete")

    def _username_search(self):
        target = self._target().replace('@','').split('.')[0]
        self.status.config(text=f"Searching username: {target}...")
        results = []
        
        # Check major platforms
        platforms = [
            ("GitHub", f"https://github.com/{target}"),
            ("Twitter", f"https://twitter.com/{target}"),
            ("Instagram", f"https://instagram.com/{target}"),
            ("Reddit", f"https://reddit.com/user/{target}"),
            ("YouTube", f"https://youtube.com/@{target}"),
            ("Twitch", f"https://twitch.tv/{target}"),
            ("Pinterest", f"https://pinterest.com/{target}"),
            ("Medium", f"https://medium.com/@{target}"),
            ("Dev.to", f"https://dev.to/{target}"),
            ("Keybase", f"https://keybase.io/{target}"),
        ]
        
        for name, url in platforms:
            try:
                req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as r:
                    if r.status == 200:
                        results.append(f"[+] {name}: {url}")
            except: pass
        
        # Sherlock
        if shutil.which("sherlock"):
            try:
                r = subprocess.run(["sherlock", target, "--print-found", "--timeout", "5"],
                        capture_output=True, text=True, timeout=60)
                for line in r.stdout.split('\n'):
                    if '[+]' in line: results.append(line.strip())
            except: pass
        
        self._log(f"Username Search: {target}", results)
        self.status.config(text="Username search complete")

    def _ip_intel(self):
        target = self._target()
        # Resolve domain to IP
        try: target = socket.gethostbyname(target)
        except: pass
        self.status.config(text=f"IP intelligence: {target}...")
        results = []
        
        # IPInfo
        try:
            req = urllib.request.Request(f"https://ipinfo.io/{target}/json", headers={'User-Agent':'CyberLab'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                for k in ['ip','city','region','country','org','loc','timezone','postal']:
                    if data.get(k): results.append(f"{k}: {data[k]}")
        except: pass
        
        # Shodan (if key available)
        key_file = os.path.expanduser("~/CyberLab/config/api_keys.json")
        if os.path.exists(key_file):
            try:
                with open(key_file) as f: keys = json.load(f)
                shodan_key = keys.get('shodan','')
                if shodan_key:
                    req = urllib.request.Request(f"https://api.shodan.io/shodan/host/{target}?key={shodan_key}")
                    with urllib.request.urlopen(req, timeout=10) as r:
                        shodan = json.loads(r.read())
                        results.append(f"Open Ports: {', '.join(str(p['port']) for p in shodan.get('data',[{}])[0].get('ports',[]))}")
            except: pass
        
        self._log(f"IP Intelligence: {target}", results)
        self.status.config(text="IP intel complete")

    def _social_search(self):
        target = self._target()
        self.status.config(text=f"Social media search: {target}...")
        results = []
        
        # Twitter/X
        try:
            req = urllib.request.Request(f"https://nitter.net/{target}", headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200: results.append("[+] Twitter/X profile found")
        except: pass
        
        # TikTok
        try:
            req = urllib.request.Request(f"https://www.tiktok.com/@{target}", headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200: results.append("[+] TikTok profile found")
        except: pass
        
        # Telegram
        try:
            req = urllib.request.Request(f"https://t.me/{target}", headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200: results.append("[+] Telegram account found")
        except: pass
        
        self._log(f"Social Media: {target}", results)
        self.status.config(text="Social search complete")

    def _tech_stack(self):
        target = self._target()
        if not target.startswith('http'): target = f"https://{target}"
        self.status.config(text=f"Analyzing tech stack...")
        results = []
        
        try:
            req = urllib.request.Request(target, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context()) as r:
                html = r.read().decode('utf-8', errors='ignore')
                headers = dict(r.headers)
                
                # Server
                if 'Server' in headers: results.append(f"Server: {headers['Server']}")
                if 'X-Powered-By' in headers: results.append(f"Powered By: {headers['X-Powered-By']}")
                
                # Framework detection
                techs = {
                    'jquery': 'jQuery', 'react': 'React', 'angular': 'Angular', 'vue': 'Vue.js',
                    'bootstrap': 'Bootstrap', 'wordpress': 'WordPress', 'drupal': 'Drupal',
                    'joomla': 'Joomla', 'laravel': 'Laravel', 'django': 'Django',
                    'flask': 'Flask', 'express': 'Express.js', 'next': 'Next.js',
                    'nuxt': 'Nuxt.js', 'gatsby': 'Gatsby', 'svelte': 'Svelte',
                }
                found = [name for key, name in techs.items() if key in html.lower()]
                if found: results.append(f"Technologies: {', '.join(set(found))}")
                
                # Security headers
                security_headers = ['X-Frame-Options','X-Content-Type-Options','Strict-Transport-Security',
                                   'Content-Security-Policy','X-XSS-Protection']
                for h in security_headers:
                    if h in headers: results.append(f"[SEC] {h}: {headers[h]}")
                    else: results.append(f"[MISS] {h}: Not set")
        except Exception as e:
            results.append(f"Error: {e}")
        
        self._log(f"Tech Stack: {target}", results)
        self.status.config(text="Tech stack complete")

    def _breach_check(self):
        target = self._target()
        self.status.config(text=f"Checking data breaches...")
        results = []
        
        if '@' in target:
            try:
                req = urllib.request.Request(f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
                        headers={'User-Agent':'CyberLab','hibp-api-key':''})
                with urllib.request.urlopen(req, timeout=10) as r:
                    if r.status == 200:
                        breaches = json.loads(r.read())
                        results.append(f"FOUND IN {len(breaches)} BREACHES:")
                        for b in breaches:
                            results.append(f"  • {b.get('Name')} - {b.get('Domain')} - {b.get('BreachDate')}")
                            if b.get('Description'): results.append(f"    {b['Description'][:100]}")
            except: results.append("No breaches found or API limit reached")
        
        self._log(f"Breach Check: {target}", results)
        self.status.config(text="Breach check complete")

    def _whois_history(self):
        target = self._target()
        self.status.config(text=f"WHOIS history...")
        results = []
        
        if shutil.which("whois"):
            try:
                r = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
                for line in r.stdout.split('\n'):
                    line = line.strip()
                    if line and any(k in line.lower() for k in ['creation','updated','expir','registrar','name','organization','email','phone','country','state','city']):
                        results.append(line)
            except: pass
        
        self._log(f"WHOIS: {target}", results[:50])
        self.status.config(text="WHOIS complete")

    def _dns_records(self):
        target = self._target()
        self.status.config(text=f"DNS enumeration...")
        results = []
        
        record_types = ['A','AAAA','MX','NS','TXT','CNAME','SOA']
        for rtype in record_types:
            if shutil.which("dig"):
                try:
                    r = subprocess.run(["dig","+short",rtype,target], capture_output=True, text=True, timeout=10)
                    if r.stdout.strip():
                        results.append(f"{rtype} Records:")
                        for line in r.stdout.strip().split('\n')[:5]:
                            results.append(f"  {line}")
                except: pass
        
        self._log(f"DNS Records: {target}", results)
        self.status.config(text="DNS complete")

    def _ssl_cert(self):
        target = self._target()
        self.status.config(text=f"SSL certificate...")
        results = []
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((target, 443), timeout=10)
            ssock = ctx.wrap_socket(sock, server_hostname=target)
            cert = ssock.getpeercert()
            
            results.append(f"Issuer: {dict(x[0] for x in cert.get('issuer',[]))}")
            results.append(f"Subject: {dict(x[0] for x in cert.get('subject',[]))}")
            results.append(f"Valid From: {cert.get('notBefore')}")
            results.append(f"Valid Until: {cert.get('notAfter')}")
            if cert.get('subjectAltName'):
                results.append("SANs:")
                for san in cert['subjectAltName']:
                    results.append(f"  {san[1]}")
            ssock.close()
        except Exception as e:
            results.append(f"SSL Error: {e}")
        
        self._log(f"SSL Certificate: {target}", results)
        self.status.config(text="SSL complete")

    def _subdomains(self):
        target = self._target()
        self.status.config(text=f"Finding subdomains...")
        results = []
        
        # crt.sh
        try:
            req = urllib.request.Request(f"https://crt.sh/?q=%25.{target}&output=json", headers={'User-Agent':'CyberLab'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                subs = set()
                for entry in data[:500]:
                    for name in entry.get('name_value','').split('\n'):
                        if target in name: subs.add(name.strip().lower().replace('*.',''))
                results = sorted(subs)[:50]
        except: pass
        
        self._log(f"Subdomains ({len(results)} found)", results)
        self.status.config(text=f"Found {len(results)} subdomains")

    def _port_scan(self):
        target = self._target()
        try: target = socket.gethostbyname(target)
        except: pass
        self.status.config(text=f"Port scanning {target}...")
        results = []
        
        common_ports = [21,22,23,25,53,80,110,143,443,465,587,993,995,1433,1521,2082,2083,2222,3306,3389,5432,5900,6379,8080,8443,8888,9000,9090,27017]
        for port in common_ports[:15]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    service = {21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',143:'IMAP',443:'HTTPS',3306:'MySQL',3389:'RDP',5432:'PostgreSQL',6379:'Redis',8080:'HTTP-Alt',8443:'HTTPS-Alt',27017:'MongoDB'}.get(port,'?')
                    results.append(f"Port {port}: OPEN ({service})")
                sock.close()
            except: pass
        
        self._log(f"Port Scan: {target}", results)
        self.status.config(text="Port scan complete")

    def _web_analysis(self):
        target = self._target()
        if not target.startswith('http'): target = f"https://{target}"
        self.status.config(text=f"Web analysis...")
        results = []
        
        try:
            req = urllib.request.Request(target, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context()) as r:
                html = r.read().decode('utf-8', errors='ignore')
                results.append(f"Status: {r.status}")
                results.append(f"Content-Type: {r.headers.get('Content-Type','?')}")
                results.append(f"Content-Length: {r.headers.get('Content-Length','?')} bytes")
                
                # Title
                title = re.findall(r'<title[^>]*>(.*?)</title>', html, re.I)
                if title: results.append(f"Title: {title[0][:100]}")
                
                # Links count
                links = len(re.findall(r'href=[\"\'](.*?)[\"\']', html))
                results.append(f"Links: {links}")
                
                # Forms
                forms = len(re.findall(r'<form', html, re.I))
                results.append(f"Forms: {forms}")
                
                # Scripts
                scripts = len(re.findall(r'<script', html, re.I))
                results.append(f"Scripts: {scripts}")
                
                # Emails found
                emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html))
                if emails: results.append(f"Emails found: {', '.join(list(emails)[:10])}")
        except Exception as e:
            results.append(f"Error: {e}")
        
        self._log(f"Web Analysis: {target}", results)
        self.status.config(text="Web analysis complete")
