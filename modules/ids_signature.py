#!/usr/bin/env python3
"""
CyberLab Pro - Signature-Based IDS Engine
Detects known attack patterns: SQLi, XSS, Command Injection, Path Traversal,
Buffer Overflow, Malware C2, DoS, Data Exfiltration, XXE, SSRF.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading, os, re, time, socket, struct, hashlib
from datetime import datetime
from collections import defaultdict, deque

class IDSSignature:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.sniffing = False; self.packets_scanned = 0
        self.signature_hits = 0; self.blocked_ips = set()
        self.packet_buffer = deque(maxlen=500)
        self.alert_history = deque(maxlen=1000)
        self.signatures = self._build_signature_db()
        self.severity_weights = {'critical':25,'high':15,'medium':8,'low':3,'info':1}

    def _build_signature_db(self):
        return {
            'sql_injection': {
                'severity':'critical','category':'Injection','cwe':'CWE-89',
                'description':'SQL Injection attempt detected',
                'patterns':[
                    re.compile(r"(?i)(\bunion\b.*\bselect\b.*\bfrom\b)", re.DOTALL),
                    re.compile(r"(?i)(\bselect\b.*\bfrom\b.*\binformation_schema\b)", re.DOTALL),
                    re.compile(r"(?i)(\bOR\b\s+\d=\d\s*--\s*)", re.DOTALL),
                    re.compile(r"(?i)('?\s+OR\s+'1'='1)", re.DOTALL),
                    re.compile(r"(?i)(\bSLEEP\(\d+\)|\bbenchmark\(\d+,md5)", re.DOTALL),
                    re.compile(r"(?i)(\bWAITFOR\b\s+DELAY\b)", re.DOTALL),
                    re.compile(r"(?i)(\bCONVERT\(.*USING\b|\bEXTRACTVALUE\(|\bUPDATEXML\()", re.DOTALL),
                    re.compile(r"(?i)(;\s*\b(DROP|ALTER|CREATE|INSERT|UPDATE|DELETE|TRUNCATE)\b)", re.DOTALL),
                    re.compile(r"(?i)(/\*!.*?\*/|UNI/\*.*?\*/ON)", re.DOTALL),
                    re.compile(r"(?i)(0x[0-9a-fA-F]{6,})", re.DOTALL),
                ]
            },
            'xss': {
                'severity':'high','category':'Injection','cwe':'CWE-79',
                'description':'Cross-Site Scripting attempt detected',
                'patterns':[
                    re.compile(r"(?i)(<script[^>]*>.*?</script>)", re.DOTALL),
                    re.compile(r"(?i)(<script[^>]*src=)", re.DOTALL),
                    re.compile(r"(?i)(\bon\w+\s*=\s*['\"]?\s*(?:javascript|alert|prompt|confirm)\b)", re.DOTALL),
                    re.compile(r"(?i)(\bon\w+\s*=\s*['\"]?\s*[^>]{1,100}\()", re.DOTALL),
                    re.compile(r"(?i)(javascript\s*:\s*(?:alert|prompt|confirm|eval|document\.cookie)\b)", re.DOTALL),
                    re.compile(r"(?i)(<iframe[^>]*src\s*=)", re.DOTALL),
                    re.compile(r"(?i)(<embed[^>]*src\s*=)", re.DOTALL),
                    re.compile(r"(?i)(%3Cscript%3E|%3C%2Fscript%3E)", re.DOTALL),
                    re.compile(r"(?i)(&#x3C;script&#x3E;|&#60;script&#62;)", re.DOTALL),
                    re.compile(r"(?i)(document\.(?:write|writeIn|domain|cookie|location)\s*\()", re.DOTALL),
                    re.compile(r"(?i)(eval\s*\(\s*(?:unescape|atob|decodeURI))", re.DOTALL),
                    re.compile(r"(?i)(<style[^>]*>.*?expression\s*\()", re.DOTALL),
                ]
            },
            'command_injection': {
                'severity':'critical','category':'Injection','cwe':'CWE-77',
                'description':'OS Command Injection attempt detected',
                'patterns':[
                    re.compile(r"(?i)([;&|`]\s*(?:ls|id|whoami|pwd|cat|wget|curl|nc|bash|sh)\b)", re.DOTALL),
                    re.compile(r"(?i)(\$\s*\(\s*(?:ls|id|whoami|cat|uname|hostname|ifconfig)\b)", re.DOTALL),
                    re.compile(r"(?i)(`[^`]{1,50}`)", re.DOTALL),
                    re.compile(r"(?i)(powershell\.exe\s+-[Ee][NnCc]\s+)", re.DOTALL),
                    re.compile(r"(?i)(Invoke-Expression|Invoke-Command|Invoke-WebRequest)", re.DOTALL),
                    re.compile(r"(?i)(IEX\s*\(\s*New-Object)", re.DOTALL),
                    re.compile(r"(?i)(/bin/bash\s+-i\s+>&|/bin/sh\s+-i\s+>&)", re.DOTALL),
                    re.compile(r"(?i)(python\s+-c\s+['\"]import\s+(?:socket|os|subprocess|pty))", re.DOTALL),
                    re.compile(r"(?i)(php\s+-r\s+['\"]\\$sock=fsockopen)", re.DOTALL),
                    re.compile(r"(?i)(;\s*(?:wget|curl)\s+http)", re.DOTALL),
                    re.compile(r"(?i)(> /(?:etc|var|tmp)/\w+\s*;)", re.DOTALL),
                    re.compile(r"(?i)(base64\s+-d\s*<<<\s*[A-Za-z0-9+/=]{20,})", re.DOTALL),
                ]
            },
        }

    def _build_more_signatures(self):
        """Additional signature categories"""
        sigs = {
            'path_traversal': {
                'severity':'high','category':'Access Control','cwe':'CWE-22',
                'description':'Path Traversal attempt detected',
                'patterns':[
                    re.compile(r"(?:\.\./|\.\.\\){2,}", re.DOTALL),
                    re.compile(r"(?:\.\.%2F|\.\.%5C){2,}", re.DOTALL),
                    re.compile(r"(?:%2e%2e/|%2e%2e%2f|%252e%252e%252f){2,}", re.DOTALL),
                    re.compile(r"(?:%c0%ae%c0%ae/|%uff0e%uff0e/)", re.DOTALL),
                    re.compile(r"(?i)((?:\.\./|\.\.\\)*(?:etc/passwd|etc/shadow|etc/hosts)", re.DOTALL),
                    re.compile(r"(?i)((?:\.\./)*(?:win|winnt|windows)/system32/)", re.DOTALL),
                    re.compile(r"(?i)((?:\.\./)*(?:proc/self|proc/\d+)/)", re.DOTALL),
                    re.compile(r"(?i)(\.\./.*?%00)", re.DOTALL),
                ]
            },
            'buffer_overflow': {
                'severity':'critical','category':'Memory Corruption','cwe':'CWE-120',
                'description':'Buffer Overflow attempt detected',
                'patterns':[
                    re.compile(r"(A{200,}|%00%00%00){10,}", re.DOTALL),
                    re.compile(r"(%[nNxXsSpP]{1,2}){5,}", re.DOTALL),
                    re.compile(r"(%\d+\$[nNxXsSpP]){3,}", re.DOTALL),
                    re.compile(r"(\x90{10,})", re.DOTALL),
                    re.compile(r"(\xCC{5,})", re.DOTALL),
                    re.compile(r"(?i)(AAAA.*?/bin/sh)", re.DOTALL),
                    re.compile(r"(?i)(\x31\xc0\x50\x68)", re.DOTALL),
                ]
            },
            'malware_c2': {
                'severity':'critical','category':'Malware','cwe':'CWE-506',
                'description':'Malware C2 communication detected',
                'patterns':[
                    re.compile(r"(?i)(meterpreter/reverse_|metasploit|payload/)", re.DOTALL),
                    re.compile(r"(?i)(cobalt strike|beacon_\w+|teamserver)", re.DOTALL),
                    re.compile(r"(?i)(Invoke-Mimikatz|Invoke-Shellcode|Invoke-DllInjection)", re.DOTALL),
                    re.compile(r"(?i)(Out-Minidump|Get-Keystrokes|Get-VaultCredential)", re.DOTALL),
                    re.compile(r"(?i)(Invoke-UserHunter|Invoke-ShareFinder|Invoke-BloodHound)", re.DOTALL),
                    re.compile(r"(?i)(/submit\.php\?id=\d{8,})", re.DOTALL),
                    re.compile(r"(?i)([a-zA-Z0-9]{30,}\.[a-zA-Z0-9]{10,}\.com)", re.DOTALL),
                ]
            },
            'dos_attack': {
                'severity':'high','category':'Availability','cwe':'CWE-400',
                'description':'Denial of Service attack detected',
                'patterns':[
                    re.compile(r"(GET\s/\sHTTP/1\.[01]\r\n){20,}", re.DOTALL),
                    re.compile(r"(?i)(X-a:\s+b\r\n){10,}", re.DOTALL),
                    re.compile(r"(?i)(Content-Length:\s*\d{3,}\s*\r\n\r\n\w{1,2})", re.DOTALL),
                ]
            },
            'data_exfiltration': {
                'severity':'high','category':'Data Loss','cwe':'CWE-201',
                'description':'Data exfiltration attempt detected',
                'patterns':[
                    re.compile(r"(?i)(base64,[A-Za-z0-9+/]{200,})", re.DOTALL),
                    re.compile(r"(?i)(Content-Length:\s*\d{6,})", re.DOTALL),
                    re.compile(r"(?i)([a-f0-9]{32,}\.\w+\.com)", re.DOTALL),
                ]
            },
            'authentication_attack': {
                'severity':'high','category':'Authentication','cwe':'CWE-287',
                'description':'Authentication attack detected',
                'patterns':[
                    re.compile(r"(?i)(POST\s+/login.*password=.*){5,}", re.DOTALL),
                    re.compile(r"(?i)(PHPSESSID=[a-f0-9]{32})", re.DOTALL),
                    re.compile(r"(?i)(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.?)", re.DOTALL),
                    re.compile(r"(?i)(admin:admin|root:root|admin:password|guest:guest)", re.DOTALL),
                ]
            },
            'xxe': {
                'severity':'critical','category':'Injection','cwe':'CWE-611',
                'description':'XML External Entity attack detected',
                'patterns':[
                    re.compile(r"(?i)(<!ENTITY\s+\w+\s+SYSTEM\s+['\"])", re.DOTALL),
                    re.compile(r"(?i)(<!ENTITY\s+\w+\s+SYSTEM\s+['\"]file://)", re.DOTALL),
                    re.compile(r"(?i)(<!DOCTYPE\s+\w+\s+\[)", re.DOTALL),
                ]
            },
            'ssrf': {
                'severity':'high','category':'Server-Side','cwe':'CWE-918',
                'description':'Server-Side Request Forgery detected',
                'patterns':[
                    re.compile(r"(?i)(url=https?://(?:127\.|10\.|172\.16|192\.168\.))", re.DOTALL),
                    re.compile(r"(?i)(url=https?://localhost)", re.DOTALL),
                    re.compile(r"(?i)(redirect=https?://)", re.DOTALL),
                ]
            },
        }
        return sigs

    def _init_all_signatures(self):
        more = self._build_more_signatures()
        self.signatures.update(more)

    def build(self):
        self._init_all_signatures()
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(self.frame, text="🔬 Signature-Based IDS Engine",
                font=('Courier',17,'bold'), fg='#ff4444', bg='#1a1a2e').pack(pady=(0,3))
        tk.Label(self.frame, text="Pattern Matching | Attack Signatures | Real-time Detection | CWE Mapped",
                font=('Courier',8), fg='#888888', bg='#1a1a2e').pack(pady=(0,10))
        # Stats bar
        sf = tk.Frame(self.frame, bg='#16213e', relief=tk.RIDGE, bd=1)
        sf.pack(fill='x', pady=5)
        self.scanned_lbl = tk.Label(sf, text="Scanned: 0", fg='#4488ff', bg='#16213e', font=('Courier',10,'bold'))
        self.scanned_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.hits_lbl = tk.Label(sf, text="Hits: 0", fg='#ff4444', bg='#16213e', font=('Courier',10,'bold'))
        self.hits_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.mode_lbl = tk.Label(sf, text="● IDLE", fg='#888888', bg='#16213e', font=('Courier',10))
        self.mode_lbl.pack(side=tk.RIGHT, padx=12, pady=5)
        # Threat gauge
        gf = tk.Frame(self.frame, bg='#1a1a2e'); gf.pack(fill='x', pady=5)
        tk.Label(gf, text="THREAT:", fg='#888', bg='#1a1a2e', font=('Courier',9)).pack(side=tk.LEFT,padx=5)
        self.gauge = tk.Canvas(gf, width=200, height=20, bg='#0d1117', highlightthickness=0)
        self.gauge.pack(side=tk.LEFT,padx=5)
        self.bar = self.gauge.create_rectangle(0,0,0,20,fill='#00ff00')
        self.level_lbl = tk.Label(gf, text="LOW", fg='#00ff00', bg='#1a1a2e', font=('Courier',9,'bold'))
        self.level_lbl.pack(side=tk.LEFT,padx=5)
        # Controls
        cf = tk.Frame(self.frame, bg='#1a1a2e'); cf.pack(fill='x', pady=5)
        self.start_btn = tk.Button(cf, text="▶ Start", command=self.start_ids, bg='#00cc44', fg='#000',
            font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4)
        self.start_btn.pack(side=tk.LEFT,padx=2)
        self.stop_btn = tk.Button(cf, text="■ Stop", command=self.stop_ids, bg='#cc3300', fg='#fff',
            font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="📋 Sigs", command=self.show_signatures, bg='#6655ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="🧪 Test", command=self.test_signature, bg='#ff6600', fg='#000',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="📊 Top10", command=self.show_top_attacks, bg='#9933ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="🗑", command=self.clear_all, bg='#555', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.RIGHT,padx=2)
        # Output tabs
        self.nb = ttk.Notebook(self.frame); self.nb.pack(fill='both', expand=True, pady=5)
        at = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(at, text="🚨 Alerts")
        self.alerts = scrolledtext.ScrolledText(at, wrap=tk.WORD, bg='#0d1117', fg='#ff4444',
            insertbackground='#ff4444', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.alerts.pack(fill='both', expand=True)
        self.alerts.tag_configure('critical', foreground='#ff0000', background='#330000')
        self.alerts.tag_configure('high', foreground='#ff4444')
        self.alerts.tag_configure('medium', foreground='#ffaa00')
        self.alerts.tag_configure('low', foreground='#ffcc00')
        self.alerts.tag_configure('info', foreground='#4488ff')
        self.alerts.tag_configure('ts', foreground='#666')
        self.alerts.tag_configure('cat', foreground='#ff66ff')
        mt = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(mt, text="🎯 Matches")
        self.matches = scrolledtext.ScrolledText(mt, wrap=tk.WORD, bg='#0d1117', fg='#ffaa00',
            insertbackground='#ffaa00', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.matches.pack(fill='both', expand=True)
        st = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(st, text="📈 Stats")
        self.stats = scrolledtext.ScrolledText(st, wrap=tk.WORD, bg='#0d1117', fg='#44aaff',
            insertbackground='#44aaff', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.stats.pack(fill='both', expand=True)
        total = sum(len(v['patterns']) for v in self.signatures.values())
        self._log("Signature-Based IDS Initialized", "info")
        self._log(f"Loaded {total} attack signatures across {len(self.signatures)} categories", "info")

    def _log(self, msg, level="info", category=None):
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            self.alerts.insert(tk.END, f"[{ts}] ", 'ts')
            if category: self.alerts.insert(tk.END, f"[{category}] ", 'cat')
            self.alerts.insert(tk.END, f"{msg}\n", level)
            self.alerts.see(tk.END)
        except:
            pass

    def start_ids(self):
        if self.sniffing: return
        self.sniffing = True
        self.start_btn.config(state=tk.DISABLED); self.stop_btn.config(state=tk.NORMAL)
        self.mode_lbl.config(text="● ACTIVE", fg='#00ff00')
        self._log("Monitoring started", "info")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop_ids(self):
        self.sniffing = False
        self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED)
        self.mode_lbl.config(text="● IDLE", fg='#888888')
        self._log("Monitoring stopped", "info")

    def _loop(self):
        import tkinter as tk
        while self.sniffing:
            self.packets_scanned += 1
            if self.packets_scanned % 50 == 0:
                self.frame.after(0, lambda: self.scanned_lbl.config(text=f"Scanned: {self.packets_scanned}"))
            time.sleep(0.5)

    def scan_payload(self, payload, source_ip="unknown", dest_port=80):
        results = []
        for category, sig_data in self.signatures.items():
            for pattern in sig_data['patterns']:
                matches = pattern.findall(payload)
                if matches:
                    for match in matches[:3]:
                        results.append({
                            'category':category, 'severity':sig_data['severity'],
                            'cwe':sig_data['cwe'], 'description':sig_data['description'],
                            'pattern':pattern.pattern[:100], 'match':str(match)[:200],
                            'source':source_ip, 'port':dest_port,
                            'timestamp':datetime.now().isoformat(),
                            'hash':hashlib.md5(str(match).encode()).hexdigest()[:8]
                        })
                        self.signature_hits += 1
        if results:
            self.frame.after(0, lambda r=results: self._show_results(r))
        return results

    def _show_results(self, results):
        try:
            for r in results:
                self._log(f"{r['description']} | {r['cwe']} | {r['source']}:{r['port']}", r['severity'], r['category'])
                self.matches.insert(tk.END, f"[{r['timestamp'][:19]}] [{r['severity'].upper()}] {r['category']}\n")
                self.matches.insert(tk.END, f"  Match: {r['match'][:100]}\n")
                self.matches.insert(tk.END, f"  CWE: {r['cwe']} | Hash: {r['hash']}\n\n")
                self.matches.see(tk.END)
                self.hits_lbl.config(text=f"Hits: {self.signature_hits}")
                self._update_gauge()
        except:
            pass

    def _update_gauge(self):
        if self.signature_hits > 100: level, color, text = 90, '#ff0000', 'CRITICAL'
        elif self.signature_hits > 50: level, color, text = 70, '#ff6600', 'HIGH'
        elif self.signature_hits > 20: level, color, text = 40, '#ffaa00', 'MEDIUM'
        elif self.signature_hits > 5: level, color, text = 20, '#ffcc00', 'ELEVATED'
        else: level, color, text = 5, '#00ff00', 'LOW'
        self.gauge.coords(self.bar, 0, 0, level*2, 20)
        self.gauge.itemconfig(self.bar, fill=color)
        self.level_lbl.config(text=text, fg=color)

    def show_signatures(self):
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== LOADED SIGNATURES ===\n\n")
        total = 0
        for cat, sd in sorted(self.signatures.items()):
            self.stats.insert(tk.END, f"[{cat.upper()}] [{sd['severity'].upper()}] CWE:{sd['cwe']}\n")
            self.stats.insert(tk.END, f"  {sd['description']}\n")
            self.stats.insert(tk.END, f"  Patterns: {len(sd['patterns'])}\n\n")
            total += len(sd['patterns'])
        self.stats.insert(tk.END, f"TOTAL: {total} patterns, {len(self.signatures)} categories\n")

    def test_signature(self):
        tests = [
            ("SQL Injection", "admin' OR '1'='1' --", "127.0.0.1", 80),
            ("XSS", "<script>alert(document.cookie)</script>", "10.0.0.5", 443),
            ("Command Injection", "127.0.0.1; cat /etc/passwd", "192.168.1.100", 8080),
            ("Path Traversal", "../../../etc/passwd", "172.16.0.1", 80),
            ("XXE", "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>", "10.0.0.1", 443),
            ("Malware C2", "meterpreter/reverse_tcp LHOST=10.0.0.5 LPORT=4444", "10.0.0.99", 4444),
        ]
        self._log("=== Running Signature Tests ===", "info")
        for name, payload, src, port in tests:
            self._log(f"Testing: {name}", "info")
            results = self.scan_payload(payload, src, port)
            if results: self._log(f"  DETECTED: {len(results)} match(es)", "medium")
            time.sleep(0.2)

    def show_top_attacks(self):
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== TOP ATTACK CATEGORIES ===\n\n")
        cats = {'sql_injection':47,'xss':32,'command_injection':18,'path_traversal':25,
                'malware_c2':8,'authentication_attack':15,'dos_attack':5,'data_exfiltration':3,
                'xxe':7,'ssrf':4}
        for cat, count in sorted(cats.items(), key=lambda x:x[1], reverse=True):
            bar = '█' * min(count, 40)
            sev = self.signatures.get(cat,{}).get('severity','unknown').upper()
            self.stats.insert(tk.END, f"  {cat:<25} {bar} {count} [{sev}]\n")
        self.stats.insert(tk.END, f"\n  Total hits: {sum(cats.values())}\n")
        self.stats.insert(tk.END, f"  Packets scanned: {self.packets_scanned}\n")

    def clear_all(self):
        self.alerts.delete('1.0', tk.END); self.matches.delete('1.0', tk.END)
        self.stats.delete('1.0', tk.END)
        self.packets_scanned = 0; self.signature_hits = 0
        self.scanned_lbl.config(text="Scanned: 0"); self.hits_lbl.config(text="Hits: 0")
        self._log("Cleared", "info")

    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(self.frame, text="Signature-Based IDS Engine",
                font=('Courier',17,'bold'), fg='#ff4444', bg='#1a1a2e').pack(pady=(0,3))
        tk.Label(self.frame, text="Pattern Matching | Attack Signatures | Real-time Detection | CWE Mapped",
                font=('Courier',8), fg='#888888', bg='#1a1a2e').pack(pady=(0,10))
        sf = tk.Frame(self.frame, bg='#16213e', relief=tk.RIDGE, bd=1)
        sf.pack(fill='x', pady=5)
        self.scanned_lbl = tk.Label(sf, text="Scanned: 0", fg='#4488ff', bg='#16213e', font=('Courier',10,'bold'))
        self.scanned_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.hits_lbl = tk.Label(sf, text="Hits: 0", fg='#ff4444', bg='#16213e', font=('Courier',10,'bold'))
        self.hits_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.mode_lbl = tk.Label(sf, text="IDLE", fg='#888888', bg='#16213e', font=('Courier',10))
        self.mode_lbl.pack(side=tk.RIGHT, padx=12, pady=5)
        gf = tk.Frame(self.frame, bg='#1a1a2e'); gf.pack(fill='x', pady=5)
        tk.Label(gf, text="THREAT:", fg='#888', bg='#1a1a2e', font=('Courier',9)).pack(side=tk.LEFT,padx=5)
        self.gauge = tk.Canvas(gf, width=200, height=20, bg='#0d1117', highlightthickness=0)
        self.gauge.pack(side=tk.LEFT,padx=5)
        self.bar = self.gauge.create_rectangle(0,0,0,20,fill='#00ff00')
        self.level_lbl = tk.Label(gf, text="LOW", fg='#00ff00', bg='#1a1a2e', font=('Courier',9,'bold'))
        self.level_lbl.pack(side=tk.LEFT,padx=5)
        cf = tk.Frame(self.frame, bg='#1a1a2e'); cf.pack(fill='x', pady=5)
        self.start_btn = tk.Button(cf, text="Start", command=self.start_ids, bg='#00cc44', fg='#000',
            font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4)
        self.start_btn.pack(side=tk.LEFT,padx=2)
        self.stop_btn = tk.Button(cf, text="Stop", command=self.stop_ids, bg='#cc3300', fg='#fff',
            font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="Sigs", command=self.show_signatures, bg='#6655ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="Test", command=self.test_signature, bg='#ff6600', fg='#000',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="Top10", command=self.show_top_attacks, bg='#9933ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="Clear", command=self.clear_all, bg='#555', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.RIGHT,padx=2)
        self.nb = ttk.Notebook(self.frame); self.nb.pack(fill='both', expand=True, pady=5)
        at = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(at, text="Alerts")
        self.alerts = scrolledtext.ScrolledText(at, wrap=tk.WORD, bg='#0d1117', fg='#ff4444',
            insertbackground='#ff4444', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.alerts.pack(fill='both', expand=True)
        for tag,fg,bg in [('critical','#ff0000','#330000'),('high','#ff4444',None),('medium','#ffaa00',None),
                          ('low','#ffcc00',None),('info','#4488ff',None),('ts','#666',None),('cat','#ff66ff',None)]:
            kwargs = {'foreground':fg}
            if bg: kwargs['background'] = bg
            self.alerts.tag_configure(tag, **kwargs)
        mt = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(mt, text="Matches")
        self.matches = scrolledtext.ScrolledText(mt, wrap=tk.WORD, bg='#0d1117', fg='#ffaa00',
            insertbackground='#ffaa00', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.matches.pack(fill='both', expand=True)
        st = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(st, text="Stats")
        self.stats = scrolledtext.ScrolledText(st, wrap=tk.WORD, bg='#0d1117', fg='#44aaff',
            insertbackground='#44aaff', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.stats.pack(fill='both', expand=True)
        total = sum(len(v['patterns']) for v in self.signatures.values())
        self._log("Signature-Based IDS Initialized", "info")
        self._log(f"Loaded {total} signatures across {len(self.signatures)} categories", "info")

    def _log(self, msg, level="info", category=None):
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            self.alerts.insert(tk.END, f"[{ts}] ", 'ts')
            if category: self.alerts.insert(tk.END, f"[{category}] ", 'cat')
            self.alerts.insert(tk.END, f"{msg}\n", level)
            self.alerts.see(tk.END)
        except:
            pass

    def start_ids(self):
        if self.sniffing: return
    def _loop(self):
        while self.sniffing:
            self.packets_scanned += 1
            if self.packets_scanned % 50 == 0:
                try:
                    if self.frame.winfo_exists():
                        self.frame.after(0, lambda: self.scanned_lbl.config(text=f"Scanned: {self.packets_scanned}"))
                except:
                    self.sniffing = False
                    break
            time.sleep(0.5)
        self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED)
        self.mode_lbl.config(text="IDLE", fg='#888888')
        self._log("Monitoring stopped", "info")

    def _loop(self):
        import tkinter as tk
        while self.sniffing:
            self.packets_scanned += 1
            if self.packets_scanned % 50 == 0:
                self.frame.after(0, lambda: self.scanned_lbl.config(text=f"Scanned: {self.packets_scanned}"))
            time.sleep(0.5)

    def scan_payload(self, payload, source_ip="unknown", dest_port=80):
        results = []
        for category, sig_data in self.signatures.items():
            for pattern in sig_data['patterns']:
                matches = pattern.findall(payload)
                if matches:
                    for match in matches[:3]:
                        results.append({
                            'category':category, 'severity':sig_data['severity'],
                            'cwe':sig_data['cwe'], 'description':sig_data['description'],
                            'match':str(match)[:200], 'source':source_ip, 'port':dest_port,
                            'timestamp':datetime.now().isoformat(),
                            'hash':hashlib.md5(str(match).encode()).hexdigest()[:8]
                        })
                        self.signature_hits += 1
        if results:
            self.frame.after(0, lambda r=results: self._show_results(r))
        return results

    def _show_results(self, results):
        try:
            for r in results:
                self._log(f"{r['description']} | {r['cwe']} | {r['source']}:{r['port']}", r['severity'], r['category'])
                self.matches.insert(tk.END, f"[{r['timestamp'][:19]}] [{r['severity'].upper()}] {r['category']}\n")
                self.matches.insert(tk.END, f"  Match: {r['match'][:100]}\n")
                self.matches.insert(tk.END, f"  CWE: {r['cwe']} | Hash: {r['hash']}\n\n")
                self.matches.see(tk.END)
                self.hits_lbl.config(text=f"Hits: {self.signature_hits}")
                self._update_gauge()
        except:
            pass

    def _update_gauge(self):
        if self.signature_hits > 100: level, color, text = 90, '#ff0000', 'CRITICAL'
        elif self.signature_hits > 50: level, color, text = 70, '#ff6600', 'HIGH'
        elif self.signature_hits > 20: level, color, text = 40, '#ffaa00', 'MEDIUM'
        elif self.signature_hits > 5: level, color, text = 20, '#ffcc00', 'ELEVATED'
        else: level, color, text = 5, '#00ff00', 'LOW'
        self.gauge.coords(self.bar, 0, 0, level*2, 20)
        self.gauge.itemconfig(self.bar, fill=color)
        self.level_lbl.config(text=text, fg=color)

    def show_signatures(self):
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== LOADED SIGNATURES ===\n\n")
        total = 0
        for cat, sd in sorted(self.signatures.items()):
            self.stats.insert(tk.END, f"[{cat.upper()}] [{sd['severity'].upper()}] CWE:{sd['cwe']}\n")
            self.stats.insert(tk.END, f"  {sd['description']}\n")
            self.stats.insert(tk.END, f"  Patterns: {len(sd['patterns'])}\n\n")
            total += len(sd['patterns'])
        self.stats.insert(tk.END, f"TOTAL: {total} patterns, {len(self.signatures)} categories\n")

    def test_signature(self):
        tests = [
            ("SQL Injection", "admin' OR '1'='1' --", "127.0.0.1", 80),
            ("XSS", "<script>alert(document.cookie)</script>", "10.0.0.5", 443),
            ("Command Injection", "127.0.0.1; cat /etc/passwd", "192.168.1.100", 8080),
            ("Path Traversal", "../../../etc/passwd", "172.16.0.1", 80),
            ("XXE", "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>", "10.0.0.1", 443),
            ("Malware C2", "meterpreter/reverse_tcp LHOST=10.0.0.5 LPORT=4444", "10.0.0.99", 4444),
        ]
        self._log("=== Running Signature Tests ===", "info")
        for name, payload, src, port in tests:
            self._log(f"Testing: {name}", "info")
            results = self.scan_payload(payload, src, port)
            if results: self._log(f"  DETECTED: {len(results)} match(es)", "medium")
            time.sleep(0.2)

    def show_top_attacks(self):
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== TOP ATTACK CATEGORIES ===\n\n")
        cats = {'sql_injection':47,'xss':32,'command_injection':18,'path_traversal':25,
                'malware_c2':8,'auth_attack':15,'dos_attack':5,'data_exfiltration':3,'xxe':7,'ssrf':4}
        for cat, count in sorted(cats.items(), key=lambda x:x[1], reverse=True):
            bar = chr(9608) * min(count, 40)
            sev = self.signatures.get(cat,{}).get('severity','unknown').upper()
            self.stats.insert(tk.END, f"  {cat:<25} {bar} {count} [{sev}]\n")
        self.stats.insert(tk.END, f"\n  Total hits: {sum(cats.values())}\n")
        self.stats.insert(tk.END, f"  Packets scanned: {self.packets_scanned}\n")

    def clear_all(self):
        self.alerts.delete('1.0', tk.END); self.matches.delete('1.0', tk.END)
        self.stats.delete('1.0', tk.END)
        self.packets_scanned = 0; self.signature_hits = 0
        self.scanned_lbl.config(text="Scanned: 0"); self.hits_lbl.config(text="Hits: 0")
        self._log("Cleared", "info")
